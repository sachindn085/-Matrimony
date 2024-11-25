from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from user.models import User
from notification.models import Notification

# Create your views here.
class MessageCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        sender= request.user
        receiver=request.data.get('receiver')
        try:
            receiver_instance=User.objects.get(username=receiver)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)
        if receiver_instance==sender:
            return Response({"error": "You cannot send message to yourself"}, status=status.HTTP_400_BAD_REQUEST)
        data=request.data.copy()
        data['receiver']=receiver_instance.pk
        
        serializer= MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(sender=sender)
            Notification.objects.create(
                user=receiver_instance,
                message=f"{sender.username} has sent you a message"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    def get(self, request):
        user= request.user
        messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
        for message in messages:
            if message.receiver == user:
                message.status = 'read'
                message.save()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
class MessageDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request,message_id):
        user = request.user
        try:
            message= Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if message.sender == user or message.receiver == user:
            message.delete()
            return Response({"message": "Message deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You are not authorized to delete this message"}, status=status.HTTP_403_FORBIDDEN)
        
        
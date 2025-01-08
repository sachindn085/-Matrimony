from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from user.models import User
from notification.models import Notification
from matching_app.models import Matching
from django.db.models import Q

# Create your views here.
class MessageCreateView(APIView):
    permission_classes = [IsAuthenticated]
    # def post(self,request):
    #     sender= request.user
    #     receiver=request.data.get('receiver')
    #     try:
    #         receiver_instance=User.objects.get(username=receiver)
    #     except User.DoesNotExist:
    #         return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)
    #     if receiver_instance==sender:
    #         return Response({"error": "You cannot send message to yourself"}, status=status.HTTP_400_BAD_REQUEST)
    #     data=request.data.copy()
    #     data['receiver']=receiver_instance.pk
        
    #     serializer= MessageSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save(sender=sender)
    #         Notification.objects.create(
    #             user=receiver_instance,
    #             message=f"{sender.username} has sent you a message"
    #         )
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def post(self,request):
        sender= request.user
        receiver=request.data.get('receiver')
        try:
            receiver_instance=User.objects.get(username=receiver)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)
        if receiver_instance==sender:
            return Response({"error": "You cannot send message to yourself"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            matching_request = Matching.objects.get(user1=sender, user2=receiver_instance,status='accepted')
        except Matching.DoesNotExist:
            return Response({"error": "You can only send messages to accepted matches"}, status=status.HTTP_400_BAD_REQUEST)
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
        
        
class MessageListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        sender=request.user
        receiver=request.data.get('receiver')
        if not receiver:
            return Response({"error": "Receiver is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            receiver_instance=User.objects.get(username=receiver)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)
        data=request.data.copy()
        data['receiver']=receiver_instance.pk
        # if sender==receiver_instance:
        #     return Response({"error": "You cannot send message to yourself"}, status=status.HTTP_400_BAD_REQUEST)
        messages= Message.objects.filter((Q(sender=sender) & Q(receiver=receiver_instance)|Q(sender=receiver_instance) & Q(receiver=sender))).order_by('created_at')
        for message in messages:
            if message.receiver == sender:
                message.status = 'read'
                message.save()
        serializers= MessageSerializer(messages, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)      


class RetriveUnreadMessagesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user=request.user
        unread_messages = Message.objects.filter(receiver=user, status='unread')
        serializer= MessageSerializer(unread_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
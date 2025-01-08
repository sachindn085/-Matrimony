from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from django.contrib.auth import get_user_model

# Create your views here.
class NotificationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        notifications.update(is_read=True)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
class SendBulkNotificationView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        message= request.data.get('message')
        if not message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
        User=get_user_model()
        users=User.objects.exclude(id=request.user.id)
        notifications=[]
        for user in users:
            notifications.append(Notification(user=user, message=message))
        Notification.objects.bulk_create(notifications)
        return Response({"message": "Notifications sent successfully"}, status=status.HTTP_201_CREATED)
    
class RetriveUnreadNotificationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user, is_read=False)
        # notifications.update(is_read=True)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
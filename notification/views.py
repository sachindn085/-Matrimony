from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NotificationSerializer
# from user.models import User
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class NotificationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        notifications.update(is_read=True)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
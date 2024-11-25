from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .models import User
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from notification.models import Notification
from message.models import Message
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        Retrieves a list of all users if the requester is a superuser.

        - If the user is authenticated and a superuser, returns a serialized list of all users.
        - If the user is not a superuser, returns an error message with a 401 Unauthorized status.
        """
        # users=User.objects.all()
        # if request.user.is_superuser:
        #     serializer = UserSerializer(users, many=True)
        #     return Response(serializer.data)
        # else:
        #     return Response({"error":"You are not authorized to view this page."}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        users = User.objects.all()  # Get all users from the database
        
        if not request.user.is_superuser:  # Check if the user is a superuser
            return Response({"error": "You are not authorized to view this page."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Pagination setup
        paginator = PageNumberPagination()
        paginator.page_size = 5  # You can adjust the page size here
        page = paginator.paginate_queryset(users, request)  # Paginate the queryset
        
        if page is not None:
            # Serialize the paginated results
            serializer = UserSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)  # Return paginated response
        
        # If no page results found (for some reason)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)  # Return all data without pagination if no page size was used.
    
class UserCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handles the creation of a new user.

        - Accepts data from the request and attempts to create a new user.
        - If the request data is valid, the user is created and a serialized response is returned.
        - If the request data is invalid, an error response is returned with details about the validation issues.

        Returns:
            Response: A JSON response containing the created user's data or errors.
        """ 
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            if user != request.user and not request.user.is_superuser:
                return Response({"error":"You are not authorized to view this page."}, status=status.HTTP_401_UNAUTHORIZED)
            # user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            if user != request.user:
                return Response({"error":"You are not authorized to view this page."}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserDeleteView(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not request.user.is_superuser:
            return Response({"error": "You are not authorized to delete users."}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Username: {username}, Password: {password}") 
        user = authenticate(request,username=request.data['username'],password=request.data['password'])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            unread_notifications = Notification.objects.filter(user=user, is_read=False)
            unread_notifications_count = unread_notifications.count()
            # notification_serializer = NotificationSerializer(unread_notifications, many=True)

            unread_messages = Message.objects.filter(receiver=user, status='unread')
            unread_messages_count = unread_messages.count()
            # message_serializer = MessageSerializer(unread_messages, many=True)
            return Response({
                'token': token.key,
                'unread_notifications_count': unread_notifications_count,
                # 'unread_notifications': notification_serializer.data,
                'unread_messages_count': unread_messages_count,
                # 'unread_messages': message_serializer.data
            }, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
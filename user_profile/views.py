from django.shortcuts import render
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


class ProfileListCreateView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]



class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer=ProfileSerializer(data=request.data)
        if serializer.is_valid():
            if Profile.objects.filter(user=request.user).exists():
                return Response({"error": "Profile already exists for this user"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        try:
            user=request.user
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)
        
class UpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def put(self, request):

        try:
            user=request.user
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)
        

    def delete(self, request):
        try:
            user=request.user
            profile = Profile.objects.get(user=request.user)
            profile.delete()
            return Response({"message": "Profile deleted successfully"}, status=204)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)
        
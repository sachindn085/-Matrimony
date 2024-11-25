from django.shortcuts import render
from .models import Preference
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PreferenceSerializer

# Create your views here.
class CreatePreferenceView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer=PreferenceSerializer(data=request.data)
        if serializer.is_valid():
            if Preference.objects.filter(user=request.user).exists():
                return Response({"error": "Preference already exists for this user"}, status=400)
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
    def get(self, request):
        user=request.user
        preference = Preference.objects.filter(user=request.user)
        serializer = PreferenceSerializer(preference, many=True)
        return Response(serializer.data)
    
class UpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        try:
            user = request.user
            preference = Preference.objects.get(user=request.user)
            serializer = PreferenceSerializer(preference, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except Preference.DoesNotExist:
            return Response({"error": "Preference not found"}, status=404)
        
    def delete(self, request):
        try:
            user=request.user
            preference = Preference.objects.get(user=request.user)
            preference.delete()
            return Response({"message": "Preference deleted successfully"}, status=204)
        except Preference.DoesNotExist:
            return Response({"error": "Preference not found"}, status=404)

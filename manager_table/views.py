from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import common_matching, Subscribe
from .serializers import  MatchingSerializer
from .serializers import SubscriptionTypeSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CommonMatchingListCreateView(generics.ListCreateAPIView):
    queryset = common_matching.objects.all()
    serializer_class = MatchingSerializer
    permission_classes = [IsAdminUser]

class CommonMatchingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = common_matching.objects.all()
    serializer_class = MatchingSerializer
    permission_classes = [IsAdminUser]


class GetMatchingView(APIView):
    def get(self, request,religion):
        try:
            matching = common_matching.objects.filter(type=religion)
            serializer = MatchingSerializer(matching, many=True)
            return Response(serializer.data)
        except common_matching.DoesNotExist:
            return Response({"error": "Matching not found"}, status=404)
        

class SubscriptionTypeCreateView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = SubscriptionTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        try:
            subscription_type = Subscribe.objects.get(pk=pk)
        except Subscribe.DoesNotExist:
            return Response({"error": "Subscription type not found"}, status=404)
        serializer= SubscriptionTypeSerializer(subscription_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user=request.user
        subscription_types = Subscribe.objects.all()
        serializer = SubscriptionTypeSerializer(subscription_types, many=True)
        return Response(serializer.data)
        
    
    def delete(self, request, pk):
        user=request.user
        try:
            subscription_type = Subscribe.objects.get(pk=pk)
        except Subscribe.DoesNot:
            return Response({"error": "Subscription type not found"}, status=404)
        if user != request.user:
            return Response({"error": "You are not authorized to delete this subscription type"}, status=403)
        subscription_type.delete()
        return Response({"message": "Subscription type deleted successfully"}, status=204)

# from django.shortcuts import render
from .models import Matching
from .serializers import MatchingSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from user.models import User
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from notification.models import Notification
from preferences.models import Preference
from subscription.models import Subscription

# Create your views here.
class MatchingCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user1 = request.user
        user2= request.data.get('user2')
        if not self.user_has_active_subscription(user1):
            return Response({"error": "You need an active subscription to send a matching request."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user2_instance = User.objects.get(username=user2)
        except User .DoesNotExist:
            return Response({'error': 'User2 not found'}, status=404)
        data=request.data.copy()
        data['user2']=user2_instance.pk
        serializer= MatchingSerializer(data=data)
        existing_match = Matching.objects.filter((Q(user1=user1) & Q(user2=user2_instance)) |(Q(user1=user2_instance) & Q(user2=user1))).first()
        if existing_match:
            return Response({"message": "Match already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if user1==user2_instance:
            return Response({"message": "Cannot match with yourself"}, status=status.HTTP_400_BAD_REQUEST)
        if user1.gender == user2_instance.gender:
            return Response({"message": "Cannot match with same gender"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(user1=user1,user2=user2_instance)
            Notification.objects.create(
                user=user2_instance,
                message=f"{user1.username} has matched with you"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        # return Response({"message": "Match created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def user_has_active_subscription(self, user):
        """Helper method to check if a user has an active subscription"""
        active_subscription = Subscription.objects.filter(user=user, status='active').first()
        return active_subscription is not None
    
    
class MatchingUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        if not self.user_has_active_subscription(request.user):
            return Response({"error": "You need an active subscription to accept a matching request."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            matching=Matching.objects.get(pk=pk,user2=request.user)
        except Matching.DoesNotExist:
            return Response({"error": "Matching not found"}, status=404)
        new_status = request.data.get('status')
        if new_status not in ['accepted']:
            return Response({"error": "Invalid status"}, status=400)
        matching.status = new_status
        Notification.objects.create(
            user=matching.user1,
            message=f"{matching.user2.username} has {new_status} your match request"
        )
        matching.save()
        return Response(MatchingSerializer(matching).data, status=status.HTTP_200_OK)
    
    def user_has_active_subscription(self, user):
        """Helper method to check if a user has an active subscription"""
        active_subscription = Subscription.objects.filter(user=user, status='active').first()
        return active_subscription is not None
    

class MatchingRejectView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        if not self.user_has_active_subscription(request.user):
            return Response({"error": "You need an active subscription to reject a matching request."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            matching=Matching.objects.get(pk=pk,user2=request.user)
        except Matching.DoesNotExist:
            return Response({"error": "Matching not found"}, status=404)
        
        new_status = request.data.get('status')
        if new_status not in ['rejected']:
            return Response({"error": "Invalid status"}, status=400)
        matching.status = new_status
        Notification.objects.create(
            user=matching.user1,
            message=f"{matching.user2.username} has {new_status} your match request"
        )
        matching.save()
        return Response(MatchingSerializer(matching).data, status=status.HTTP_200_OK)
    
    def user_has_active_subscription(self, user):
        """Helper method to check if a user has an active subscription"""
        active_subscription = Subscription.objects.filter(user=user, status='active').first()
        return active_subscription is not None
    
class MatchingListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if not self.user_has_active_subscription(user):
            return Response({"error": "You need an active subscription to access matches."}, status=status.HTTP_400_BAD_REQUEST)
        matching = Matching.objects.filter(Q(user1=user)|Q(user2=user))
        serializer = MatchingSerializer(matching, many=True)
        return Response(serializer.data)
    
    def user_has_active_subscription(self, user):
        """Helper method to check if a user has an active subscription"""
        active_subscription = Subscription.objects.filter(user=user, status='active').first()
        return active_subscription is not None
    
    # def delete(self, request, pk):
    #     try:
    #         matching = Matching.objects.get(pk=pk)
    #     except Matching.DoesNotExist:
    #         return Response({"error": "Matching not found"}, status=404)
    #     matching.delete()
    #     return Response({"message": "Matching deleted successfully"}, status=204)
    
class MatchingRetriveView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user 
            # user=User.objects.get(id=user_id)
            if not self.user_has_active_subscription(user):
                return Response({"error": "You need an active subscription to access matches."}, status=status.HTTP_400_BAD_REQUEST)
            user_preference= Preference.objects.get(user=user)
            potential_matches = User.objects.exclude(id=user.id)
            potential_matches=potential_matches.filter(
                profile__gender = user_preference.gender,
                # profile__age__gte = user_preference.min_age,
                # profile__age__lte = user_preference.max_age,
                # profile__height__gte = user_preference.min_height,
                # profile__height__lte = user_preference.max_height,
                # profile__weight__gte = user_preference.min_weight,
                # profile__weight__lte = user_preference.max_weight,
                # profile__religion = user_preference.religion,
                # profile__caste = user_preference.caste
                )
            match_data =[]
            for match in potential_matches:
                match_data.append({
                    'id': match.id,
                    'username': match.username,
                    'email': match.email,
                    'profile': {
                        'name': match.profile.name,
                        'gender': match.profile.gender,
                        'age': match.profile.age,
                        'height': match.profile.height,
                        'weight': match.profile.weight,
                        'religion': match.profile.religion,
                        'caste': match.profile.caste,
                        'language':match.profile.languages,
                        'location':match.profile.location
                    }
                })
            return Response(match_data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Preference.DoesNotExist:
            return Response({"error": "User preference not found"}, status=status.HTTP_404_NOT_FOUND)
    def user_has_active_subscription(self, user):
        """Helper method to check if a user has an active subscription"""
        active_subscription = Subscription.objects.filter(user=user, status='active').first()
        return active_subscription is not None
        

        







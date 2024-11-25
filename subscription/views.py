from django.shortcuts import render
from .models import Subscription
from .serializers import SubscriptionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from manager_table.models import Subscribe
from django.utils import timezone
from notification.models import Notification

# Create your views here.
class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user= request.user
        subscription_type = request.data.get('subscription_type')
        valid_subscription_types = Subscribe.objects.filter(type='subscription').values_list('name', flat=True)
        if subscription_type not in valid_subscription_types:
            return Response({'error': f"Invalid subscription_type. Valid values are: {', '.join(valid_subscription_types)}"})
        subscribe= Subscribe.objects.get(name=subscription_type)
        start_date = timezone.now().date()
        end_date = start_date + timezone.timedelta(days=subscribe.duration)
        subscription=Subscription(
            user=user,
            subscription_type=subscription_type,
            start_date=start_date,
            end_date=end_date,
            status='active'

        )
        subscription.save()
        Notification.objects.create(
            user=user,
            message=f"Subscription {subscription_type} has been purchased"
        )
        serializer=SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def get(self, request):
        user=request.user
        subscriptions=Subscription.objects.filter(user=user)
        subscription_data = []
        for subscription in subscriptions:
            days_left =0
            if subscription.end_date:
                remaining_days = (subscription.end_date - timezone.now().date()).days
                days_left = max(remaining_days, 0)
            subscription_information = {
                'subscription_type': subscription.subscription_type,
                'start_date': subscription.start_date,
                'end_date': subscription.end_date,
                'status': subscription.status,
                'days_left': days_left
            }
            subscription_data.append(subscription_information)
        return Response(subscription_data, status=status.HTTP_200_OK)

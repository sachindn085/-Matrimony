from .models import *
from rest_framework import serializers

class MatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_matching
        fields = '__all__'

class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'
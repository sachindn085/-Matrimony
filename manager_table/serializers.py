from .models import *
from rest_framework import serializers

class MatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_matching
        fields = '__all__'

    def validate_name(self, name):
        if common_matching.objects.filter(name=name).exists():
            raise serializers.ValidationError("A matching with this name already exists.")
        return name

class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'

    

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be a positive integer.")
        return value
        
    def validate_name(self,name):
        if Subscribe.objects.filter(name=name).exists():
            raise serializers.ValidationError("A subscription with this name already exists.")
        return name
        

    
        
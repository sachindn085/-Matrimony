from rest_framework import serializers
from .models import Matching

class MatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matching
        fields = '__all__'
        read_only_fields = ['user1']


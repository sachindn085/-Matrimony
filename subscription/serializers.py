from rest_framework import serializers
from .models import Subscription
from manager_table.models import Subscribe


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

    
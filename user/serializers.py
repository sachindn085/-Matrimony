from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_fields = {'password': {'write_only':'True'}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user= User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance,validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    

# class PasswordUpdateSerializer(serializers.Serializer):
#     current_password = serializers.CharField(write_only=True)
#     new_password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)


    # def validate_current_password(self,value):
    #     User=self.context['request'].user
    #     if not User.check_password(value):
    #         raise serializers.ValidationError("Current password is incorrect.")
    #     return value
    
    # def validate(self, data):
    #     if data['new_password'] != data['confirm_password']:
    #         raise serializers.ValidationError("New password and confirm password do not match.")
    #     try:
    #         validate_password(data['current_password'])
    #     except Exception as e:
    #         raise serializers.ValidationError({"new_pasword":e.message})
    #     return data





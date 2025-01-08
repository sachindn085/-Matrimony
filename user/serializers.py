from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_fields = {'password': {'write_only':'True'}}

    def validate_age(self, value):
        if value < 18 or value > 60 :
            raise serializers.ValidationError("Age must be between 18 and 60.")

    
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
    
    def validate_password(self,password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not self.contains_uppercase(password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not self.contains_lowercase(password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not self.contains_digit(password):
            raise ValueError("Password must contain at least one digit.")
        if not self.contains_special_character(password):
            raise ValueError("Password must contain at least one special character.")
        
        
    
    def contains_uppercase(self, password):
        return any(char.isupper() for char in password)
    def contains_lowercase(self, password):
        return any(char.islower() for char in password)
    def contains_digit(self, password):
        return any(char.isdigit() for char in password)
    def contains_special_character(self, password):
        special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return any(char in special_characters for char in password)
    

# class PasswordUpdateSerializer(serializers.Serializer):
#     current_password = serializers.CharField(write_only=True)
#     new_password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)


#     def validate_current_password(self,value):
#         User=self.context['request'].user
#         if not User.check_password(value):
#             raise serializers.ValidationError("Current password is incorrect.")
#         return value
    
#     def validate(self, data):
#         if data['new_password'] != data['confirm_password']:
#             raise serializers.ValidationError("New password and confirm password do not match.")
#         try:
#             validate_password(data['current_password'])
#         except Exception as e:
#             raise serializers.ValidationError({"new_pasword":e.message})
#         return data





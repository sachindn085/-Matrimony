from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True,validators=[RegexValidator(r'^\+??\d{9,15}$',message="phone number must be emtered in the format:'+9999999999'.Up to 15 digits allowed.")])
    date_of_birth = models.DateField(blank=True, null=True)
    # gender_choices = [
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    #     ('O', 'Other'),
    # ]
    role_choices = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    # gender= models.CharField(max_length=1, choices=gender_choices, blank=True, null=True)
    role = models.CharField(max_length=10, choices=role_choices, default='user')
    is_active = models.BooleanField(default=True)
    # password_updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if self.date_of_birth:
            today = timezone.now().date()
            age = today.year - self.date_of_birth.year-((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

            if age < 18 or age > 65:
                raise ValidationError("Age must be between 18 and 65.")
            
        if self.role=='admin':
            self.is_staff=True
            self.is_superuser=True
        else:
            self.is_staff=False
            self.is_superuser=False

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()} "
    
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
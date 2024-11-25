from django.db import models
from django.utils import timezone
from notification.models import Notification

# Create your models here.
class Subscription(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING,related_name='user')
    subscription_type = models.CharField(max_length=50)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status_choices = [
        ('active','Active'),
        ('expired','Expired'),
    ]   
    status = models.CharField(max_length=10, choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} subscribed to {self.subscription_type}"
    
    def check_expiration(self):
        """Check if the subscription is expired and update status."""
        if self.end_date and self.end_date < timezone.now().date():
            self.status = 'expired'
            self.save()
            Notification.objects.create(
                user=self.user,
                message=f"Your {self.subscription_type} subscription has expired."
            )

    def save(self, *args, **kwargs):
        # Before saving the subscription, check if it should be expired
        self.check_expiration()
        super().save(*args, **kwargs)

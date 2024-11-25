from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, related_name='sender')
    receiver = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, related_name='receiver')
    message_text = models.TextField()
    status_choices = [
        ('read', 'Read'),
        ('unread', 'Unread'),
    
    ]
    status= models.CharField(max_length=20, choices=status_choices, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

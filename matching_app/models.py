# from typing import Iterable
from django.db import models
from .utils import calculate_matching_score

# Create your models here.
class Matching(models.Model):
    user1 = models.ForeignKey('user.User',on_delete=models.DO_NOTHING, related_name='user1')
    user2 = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, related_name='user2')
    score = models.IntegerField(default=0)
    status_choices = [
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.score = calculate_matching_score(self.user1, self.user2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user1.username} matched with{self.user2.username}"

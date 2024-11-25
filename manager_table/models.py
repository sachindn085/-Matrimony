from typing import Iterable
from django.db import models
from django.db.models import Max

# Create your models here.
class common_matching(models.Model):
    FIELD_TYPES= [
        ('gender','Gender'),
        ('religion','Religion'),
        ('caste','Caste'),
        ('profession','Profession'),
        ('education','Education'),
        ('location','Location'),
        ('language','Language'),
        ('marital_status','Marital_status')
    ]
    type = models.CharField(max_length=50, choices=FIELD_TYPES)
    code = models.CharField(max_length=50,unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    display_name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.display_name}({self.type})"
    
    def save(self,*args, **kwargs):
        if not self.code:
            PREFIXES = {
                'gender': 'GE',
                'religion': 'RE',
                'caste': 'CA',
                'profession': 'PR',
                'education': 'ED',
                'location': 'LO',
                'language': 'LA',
                'marital_status': 'MS',
            }
            prefix = PREFIXES.get(self.type,'xx')
            last_code = common_matching.objects.filter(type=self.type).aggregate(Max('code'))['code__max']
            if last_code and last_code.startswith(prefix):
                last_number = int(last_code[len(prefix):])
                new_number = last_number + 1
            else:
                new_number = 1
            self.code = f"{prefix}{new_number:03}"
        super().save(*args, **kwargs) 



class Subscribe(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    duration = models.IntegerField(help_text="durations in days",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    

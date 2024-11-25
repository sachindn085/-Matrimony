from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
class Preference(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.DO_NOTHING,null=True,blank=True,related_name='preference')
    min_age =  models.IntegerField(null=True, blank=True)
    max_age =  models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    caste = models.CharField(max_length=50, null=True, blank=True)
    profession = models.CharField(max_length=50, null=True, blank=True)
    education = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    min_height = models.DecimalField(help_text="height in centimeters(Cm)",max_digits=5, decimal_places=2, null=True, blank=True)
    max_height = models.DecimalField(help_text="height in centimeters(Cm)", max_digits=5, decimal_places=2, null=True, blank=True)
    min_weight = models.DecimalField(help_text="weight in kilograms(Kg)",max_digits=5, decimal_places=2, null=True, blank=True)
    max_weight = models.DecimalField(help_text="weight in kilograms(Kg)", max_digits=5, decimal_places=2, null=True, blank=True)

    min_annual_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    max_annual_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


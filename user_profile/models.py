from django.db import models
from django.utils import timezone
from user.models import User

# from matrimony.user.models import User



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.DO_NOTHING,null=True,blank=True,related_name='profile')
    name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    weight = models.DecimalField(help_text="weight in kilograms(Kg)",max_digits=5, decimal_places=2)
    height = models.DecimalField(help_text="heigth in centimeters(Cm)",max_digits=5, decimal_places=2)
    gender = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    caste = models.CharField(max_length=50, null=True, blank=True)
    profession = models.CharField(max_length=50, null=True, blank=True)
    languages = models.CharField(max_length=20, null=True, blank=True)
    education = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    marital_status = models.CharField(max_length=20, null=True, blank=True)
    Status = models.BooleanField(default=True)
    age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    '''The calculate_age method calculates a person's age based on their date_of_birth. 
       It first checks if a birthdate exists, then compares the current date with the birthdate to determine the age. 
       If the person hasn't yet had their birthday this year, it subtracts one from the age. The method returns the calculated age.'''
    
    def calculate_age(self):
        # Check if the date_of_birth attribute exists
        if self.date_of_birth:
            # Get the current date
            today = timezone.now().date()
            # Calculate the initial age by subtracting the birth year from the current year
            age = today.year - self.date_of_birth.year
            # Check if the current date hasn't yet reached the birthday for this year
            if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                # Subtract 1 from age if the birthday hasn't occurred yet this year
                age -= 1
            # Return the calculated age
            return age
        
        '''The save method calculates the person's age by calling calculate_age and assigns it to the age attribute. 
           Then, it saves the object to the database using the parent class's save method.'''
        
    def save(self, *args, **kwargs):
        self.date_of_birth = self.user.date_of_birth
        self.age=self.calculate_age()
        super().save(*args, **kwargs)
        

        
    

    



from .models import Preference
from rest_framework import serializers
from manager_table.models import common_matching

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'
        read_only_fields = ['user']


    def validate(self, data):
        gender = data.get('gender')
        religion = data.get('religion')
        caste = data.get('caste')
        profession = data.get('profession')
        education = data.get('education')
        location = data.get('location')
        language = data.get('language')
        min_age = data.get('min_age')
        max_age = data.get('max_age')

        if min_age is not None and max_age is not None and min_age > max_age:
            raise serializers.ValidationError("Minimum age cannot be greater than maximum age.")



        gender_type= common_matching.objects.filter(type='gender').values_list('name',flat=True)
        if gender not in gender_type:
            raise serializers.ValidationError(f"Invalid gender value.valid values are: {','.join(gender_type)}")
        
        
        religion_type = common_matching.objects.filter(type='religion').values_list('name', flat=True)
        if religion not in religion_type:
            raise serializers.ValidationError(f"Invalid religion value.valid values are: {', '.join(religion_type)}")
        
        caste_type = common_matching.objects.filter(type='caste').values_list('name', flat=True)
        if caste not in caste_type:
            raise serializers.ValidationError(f"Invalid caste value.valid values are: {', '.join(caste_type)}")
        
        profession_type = common_matching.objects.filter(type='profession').values_list('name', flat=True)
        if profession not in profession_type:
            raise serializers.ValidationError(f"Invalid profession value.valid values are: {', '.join(profession_type)}")
        
        education_type = common_matching.objects.filter(type='education').values_list('name', flat=True)
        if education not in education_type:
            raise serializers.ValidationError(f"Invalid education value.valid values are: {', '.join(education_type)}")
        
        
        location_type = common_matching.objects.filter(type='location').values_list('name', flat=True)
        if location not in location_type:
            raise serializers.ValidationError(f"Invalid location value.valid values are: {', '.join(location_type)}")
        
        
        language_type = common_matching.objects.filter(type='language').values_list('name', flat=True)
        if language not in language_type:
            raise serializers.ValidationError(f"Invalid language value.valid values are: {', '.join(language_type)}")
        
        return data
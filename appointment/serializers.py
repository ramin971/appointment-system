from rest_framework import serializers
from .models import Doctor,Patient


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['user','fee']
        read_only_fields = ['user']
        
    def validate(self, attrs):
        attrs['user'] = self.context.get('user')
        return super().validate(attrs)
    
    def create(self, validated_data):
        obj , _ = Doctor.objects.update_or_create(user=self.context.get('user'),defaults={'fee': validated_data['fee']})
        return obj
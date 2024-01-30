from rest_framework import serializers
from .models import Doctor,Patient


class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Doctor
        fields = ['full_name','fee']

    def get_full_name(self,obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
        
    def validate(self, attrs):
        attrs['user'] = self.context.get('user')
        return super().validate(attrs)
    
    # def create(self, validated_data):
    #     obj , _ = Doctor.objects.update_or_create(user=self.context.get('user'),defaults={'fee': validated_data['fee']})
    #     return obj
class CreateDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['user','fee']


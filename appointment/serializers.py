import jdatetime
from rest_framework import serializers,status
from .models import Doctor,Patient,MeetingTime
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class DoctorSerializer(serializers.ModelSerializer):
    # full_name = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.CharField(source='__str__')
    class Meta:
        model = Doctor
        fields = ['full_name','fee']

    # def get_full_name(self,obj):
    #     return f'{obj.user.first_name} {obj.user.last_name}'
        
    def validate(self, attrs):
        # if self.context.get('user') is not None:
        attrs['user'] = self.context.get('user')
        return super().validate(attrs)
    
    # def create(self, validated_data):
    #     obj , _ = Doctor.objects.update_or_create(user=self.context.get('user'),defaults={'fee': validated_data['fee']})
    #     return obj
class CreateDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['user','fee']


class PatientSerializer(serializers.ModelSerializer):
    meeting_time = serializers.StringRelatedField(source='time',read_only=True)
    doctor_name = serializers.StringRelatedField(source='doctor',read_only=True)
    meeting_date = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Patient
        fields = ['id','fullname','national_code','phone','doctor_name','doctor','date','meeting_date','time','meeting_time','tracking_code','created']
        read_only_fields = ['id','created','tracking_code']
        extra_kwargs = {'time':{'write_only':True,'allow_null':False},'doctor':{'write_only':True},'date':{'write_only':True}}
        
    def get_meeting_date(self,obj):
        date = obj.date
        date2j = jdatetime.date.fromgregorian(year=date.year,month=date.month,day=date.day)
        return str(date2j)


class BulkCreateMeetingTimeSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        times = [MeetingTime(**item) for item in validated_data]
        return MeetingTime.objects.bulk_create(times)
        

class MeetingTimeSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()
    class Meta:
        model = MeetingTime
        fields = ['id','time','doctor']
        read_only_fields = ['id']
        list_serializer_class = BulkCreateMeetingTimeSerializer

    def validate(self, attrs):
        attrs['doctor'] = self.context['doctor']
        return super().validate(attrs)
    

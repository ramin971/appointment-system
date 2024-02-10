from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True)
    fee = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}' 


class MeetingTime(models.Model):
    time = models.CharField(max_length=20,unique=True)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.time
    

class Patient(models.Model):
    fullname = models.CharField(max_length=50)
    national_code=models.CharField(validators=[RegexValidator(regex='^\d{10}$',message='must be 10 \
        digit',code='invalid_national_code')],max_length=10)
    phone = models.CharField(validators=[RegexValidator(regex='(\+98|0)?(9\d{9})')],max_length=13)
    date = models.DateField()
    time = models.ForeignKey(MeetingTime,on_delete=models.SET_NULL,null=True,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(Doctor,on_delete=models.PROTECT,related_name='patients')
    tracking_code = models.CharField(max_length=16,validators=[RegexValidator(regex='^\d{16}$'
                                                                              ,message='must be 16 digit'
                                                                              ,code='invalid_tc_code')]
                                                                              ,null=True,unique=True)

    def __str__(self) -> str:
        return self.fullname
    
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['date','time'],name='unique_meet_time')
        ]


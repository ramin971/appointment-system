from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest
import jdatetime
from django.contrib import admin
from appointment.models import Doctor, Patient , MeetingTime



@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_select_related = ['time','doctor__user']
    list_display = ['fullname','national_code','phone','jdate','time','doctor','tracking_code','created']
    readonly_fields = ['tracking_code','national_code']
    ordering = ['-date','time']
    list_per_page = 10
    search_fields = ['national_code','fullname']
    list_filter =['doctor','date']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).filter(tracking_code__isnull=False)

    def jdate(self,obj):
        date = obj.date
        date2j = jdatetime.date.fromgregorian(year=date.year,month=date.month,day=date.day)
        return str(date2j)

@admin.register(MeetingTime)
class MeetingTimeAdmin(admin.ModelAdmin):
    list_display = ['doctor','time']
    list_filter = ['doctor']
    
admin.site.register(Doctor)

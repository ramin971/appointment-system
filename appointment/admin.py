from django.contrib import admin

from appointment.models import Doctor, Patient

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)

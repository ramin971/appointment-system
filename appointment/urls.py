from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'doctor', views.DoctorViewSet)
# router.register(r'patient',views.PatientViewSet)
router.register(r'time',views.MeetingTimeViewSet,basename='meeting_time')
urlpatterns = [
    path('',include(router.urls)),
    path('patient/',views.PatientViewSet.as_view())
]

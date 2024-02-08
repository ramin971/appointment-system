from django.urls import path
from . import views

urlpatterns = [
    path('go-to-gateway/',views.go_to_gateway_view,name='go-to-gateway'),
    path('callbak-gateway/',views.callback_gateway_view,name='callback-gateway')
]
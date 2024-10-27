# hrm_project/urls.py

from django.urls import path
import notifications.views as hrm_views

urlpatterns = [
  
    path('register-device-token/', hrm_views.register_device_token, name='register_device_token'),
]

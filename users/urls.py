from django.urls import path
from .views import RegisterView, RequestResetPasswordView, ResetPasswordView
from rest_framework.urlpatterns import format_suffix_patterns


#url path /api/user/*

urlpatterns = [
    path('register', RegisterView.as_view(), name="user_register"),
    path('request-reset-password', RequestResetPasswordView.as_view(), name="request-reset-password"),
    path('reset-password', ResetPasswordView.as_view(), name="reset-password"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
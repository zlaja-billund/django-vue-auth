from django.urls import path
from .views import RegisterView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('register', RegisterView.as_view(), name="user_register")
]


urlpatterns = format_suffix_patterns(urlpatterns)
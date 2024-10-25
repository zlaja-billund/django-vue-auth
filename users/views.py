from rest_framework import generics
from .serializers import RegisterSerializer
from .models import User


# Create your views here.
class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
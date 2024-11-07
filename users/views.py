import os

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import RegisterSerializer, ResetPasswordSerializer
from .models import User, PasswordReset


# Create your views here.
class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        # If request requst email is missing return validation error
        try:
            email = request.data['email']
        except:
            raise ValidationError({"error": "Bad request input"})

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({'error': 'User with credentials not found'})

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Insert new password reset object in db
        PasswordReset.objects.update_or_create(
            user=user,
            defaults={'token': token}
        )

        reset_url = f"{os.environ['PASSWORD_RESET_BASE_URL']}/{token}"

        # TODO: implement here to send an email

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


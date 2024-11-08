import os

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.serializers import serialize

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from .serializers import RegisterSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer
from .models import User, PasswordReset


# Create your views here.
class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class RequestResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data['email']

        try:
            user = User.objects.get(email=email)
        except:
            raise ValidationError({'error': 'User with credentials not found'})

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Insert new password reset object in db
        PasswordReset.objects.update_or_create(
            user=user,
            defaults={'token': token}
        )

        reset_url = f"{os.environ['PASSWORD_RESET_BASE_URL']}/{token}"
        print(reset_url)

        # TODO: implement here to send an email

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        new_password = data['new_password']
        confirm_password = data['confirm_password']
        token = data['token']

        if new_password != confirm_password:
            raise ValidationError({"error": "Passwords do not match"})

        try:
            reset_obj = PasswordReset.objects.get(token=token)
        except:
            raise ValidationError({"error": "Invalid Token"})

        if reset_obj.user:
            reset_obj.user.set_password(request.data['new_password'])
            reset_obj.user.save()

            reset_obj.delete()

            return Response(data={"success": "Password updated"}, status=HTTP_200_OK)
        else:
            return Response({"error": "No user found"}, status=HTTP_404_NOT_FOUND)


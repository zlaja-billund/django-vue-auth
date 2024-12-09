import os
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from .serializers import RegisterSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer
from .models import User, PasswordReset
from services.email_handler import EmailHandler


# Create your views here.
class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class RequestResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        # Validate data and parameter
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data['email']

        # Find user with this e-mail
        try:
            user = User.objects.get(email=email)
        except:
            raise ValidationError({'error': 'User with credentials not found'})

        # Generate token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Create new password reset object in db
        PasswordReset.objects.update_or_create(
            user=user,
            defaults={'token': token}
        )

        reset_url = f"{os.environ['PASSWORD_RESET_BASE_URL']}/{token}" # Generate url with token
        print(reset_url) # print url in console using for copy and paste in browser

        # Sending requested email
        email_status = EmailHandler.send_request_reset_password( user_email=user.email, reset_password_url=reset_url )

        #if email status is failed
        if not email_status:
            return Response(data={'error', 'Email not send, please contact support team'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        # Validate data and parameter
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        new_password = data['new_password']
        confirm_password = data['confirm_password']
        token = data['token']

        # Check new password and confirm password matching
        if new_password != confirm_password:
            raise ValidationError({"error": "Passwords do not match"})

        # Get data from PasswordReset table by token
        try:
            reset_obj = PasswordReset.objects.get(token=token)
        except:
            raise ValidationError({"error": "Invalid Token"})

        # Update new user password ann delete PasswordReset item from db
        if reset_obj.user:
            reset_obj.user.set_password(request.data['new_password'])
            reset_obj.user.save()

            reset_obj.delete()

            return Response(data={"success": "Password updated"}, status=HTTP_200_OK)
        else:
            return Response({"error": "No user found"}, status=HTTP_404_NOT_FOUND)


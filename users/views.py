import os

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ResetPasswordSerializer
from .models import User, PasswordReset


# Create your views here.
class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ResetPasswordView(generics.GenericAPIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        try:
            email = request.data['email']
        except:
            return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user:
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
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)


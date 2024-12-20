from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
                required=True,
                validators=[UniqueValidator(queryset=User.objects.all())]
             )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')

        extra_kwargs = {
            'password': { 'write_only': True },
            'first_name': {'required': True},
            'last_name': { 'required': True }
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        write_only=True,
        error_messages={
            'invalid': ('Password must be at least 8 characters long with at least one capital letter and symbol')}
    )

    confirm_password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(required=True)


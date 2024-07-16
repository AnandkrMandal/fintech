from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress  # type: ignore
from .models import IPO


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# login with email and password

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    is_admin = serializers.BooleanField(read_only=True)


    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if not user:
                msg = _('User not found or invalid credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            
            # Check if the email is verified
            try:
                email_address = EmailAddress.objects.get(user=user, email=email)
                if not email_address.verified:
                    msg = _('Email is not verified.')
                    raise serializers.ValidationError(msg, code='authorization')
            except EmailAddress.DoesNotExist:
                msg = _('Email is not verified.')
                raise serializers.ValidationError(msg, code='authorization')
            
            # Check if the user is an admin
            is_admin = user.is_staff or user.is_superuser

        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        data['is_admin'] = is_admin
        return data



class IPOSerializer(serializers.ModelSerializer):
    company_logo = serializers.ImageField(use_url=True)
    rhp_pdf = serializers.FileField(use_url=True)
    drhp_pdf = serializers.FileField(use_url=True)
    
    
    class Meta:
        model = IPO
        fields = '__all__'

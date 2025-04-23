# authentication/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import PortfolioUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        label='Confirm password'
    )

    class Meta:
        model = PortfolioUser
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioUser
        fields = ['id', 'username', 'email', 'quick_id', 'date_joined']
        read_only_fields = ['id', 'quick_id', 'date_joined']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['quick_id'] = user.quick_id
        token['is_admin'] = user.is_staff
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user': UserSerializer(self.user).data,
            'refresh_exp': self.user.refresh_token_expiration,
            'access_exp': self.user.access_token_expiration
        })
        return data
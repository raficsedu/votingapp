from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email'],
                message='This Email is already taken'
            )
        ]

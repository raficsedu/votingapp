from rest_framework import serializers
from .models import Entity


class EmployerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True, source="user.first_name")
    last_name = serializers.CharField(read_only=True, source="user.last_name")
    email = serializers.CharField(read_only=True, source="user.email")
    username = serializers.CharField(read_only=True, source="user.username")

    class Meta:
        model = Entity
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'age', 'gender', 'phone', 'created_at']

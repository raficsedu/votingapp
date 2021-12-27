from rest_framework import serializers
from .models import Entity, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True, source="user.email")
    username = serializers.CharField(read_only=True, source="user.username")

    class Meta:
        model = Entity
        fields = ['id', 'username', 'email', 'name', 'address', 'phone', 'created_at']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'item', 'price', 'created_at']

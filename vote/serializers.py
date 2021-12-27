from rest_framework import serializers
from .models import Entity
from restaurant.models import Entity as R_Entity


class VoteSerializer(serializers.ModelSerializer):
    restaurant = serializers.SlugRelatedField(queryset=R_Entity.objects.all(), slug_field='id')

    class Meta:
        model = Entity
        fields = ['id', 'restaurant', 'vote', 'created_at']

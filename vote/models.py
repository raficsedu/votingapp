from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Entity(models.Model):
    employer = models.ForeignKey('employer.Entity', on_delete=models.CASCADE, related_name='employer_votes')
    restaurant = models.ForeignKey('restaurant.Entity', on_delete=models.CASCADE, related_name='restaurant_votes')
    VOTE = (
        (1, 'Liked'),
        (2, 'Not Liked')
    )
    vote = models.IntegerField('Vote', choices=VOTE, default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.employer.user.first_name + ', ' + self.restaurant.name

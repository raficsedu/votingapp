from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Entity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer')
    age = models.IntegerField('Age', null=True, blank=True)
    GENDER = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other')
    )
    gender = models.IntegerField('Gender', choices=GENDER, default=1)
    phone = models.CharField('Phone', max_length=25, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.email + ', ' + self.user.first_name + ', ' + self.phone

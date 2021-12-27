from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Entity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField('Name', max_length=255)
    address = models.CharField('Address', max_length=255, null=True, blank=True)
    phone = models.CharField('Phone', max_length=25, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.email + ', ' + self.name + ', ' + self.phone


class Menu(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='menus')
    item = models.CharField('Item Name', max_length=255)
    price = models.FloatField('Price', default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.entity.name + ', ' + self.item + ', ' + str(self.price)

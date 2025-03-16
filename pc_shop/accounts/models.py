from django.db import models
from django.contrib.auth.models import User
from configurator.models import PCBuild

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    favorite_products = models.ManyToManyField('catalog.Product', blank=True, related_name='favorited_by')
    saved_builds = models.ManyToManyField(PCBuild, blank=True, related_name='saved_by')

    def __str__(self):
        return f"Профиль: {self.user.username}"
from django.db import models
from django.contrib.auth.models import User
from configurator.models import PCBuild

class CommunityBuild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pc_build = models.OneToOneField(PCBuild, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[('gaming', 'Игровая'), ('office', 'Офисная')])
    rating = models.FloatField(default=0)
    votes = models.ManyToManyField(User, related_name='voted_builds', blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    build = models.ForeignKey(CommunityBuild, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user.username}"
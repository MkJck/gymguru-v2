from django.db import models

from django.contrib.auth import get_user_model
from django.db import transaction
import random

User = get_user_model()

class Timeline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timelines')
    name = models.CharField(max_length=100)
    # settings = models.JSONField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    class Meta:
        unique_together = ['user', 'name']


class TimelineType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
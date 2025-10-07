from django.db import models

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class Timeline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timelines')
    name = models.CharField(max_length=100)
    # settings = models.JSONField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_timeline_user_name')
        ]

    def validate_name(self, value):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not user or user.is_anonymous:
            return value  # если нет авторизации, пропускаем

        qs = Timeline.objects.filter(user=user, name=value, is_deleted=False)
        if self.instance:  # при обновлении исключаем сам объект
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("You already have timeline with that name.")

        return value

    def validate(self, attrs):
        if self.instance and self.instance.is_deleted:
            raise serializers.ValidationError("You can't edit deleted timeline")
        return attrs

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not self.instance and user and not user.is_anonymous:
            count = Timeline.objects.filter(user=user, is_deleted=False).count()
            if count >= 10:
                raise serializers.ValidationError("You can't create more than 10 timelines.")
        return attrs





class TimelineType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
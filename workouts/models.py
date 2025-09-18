from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# class Set(models.Model):
#     exercise
#     value
#     set_number
#     weight
#     reps
#     duration
#     is_completed


# class Exercise(models.Model):
#     workout = models.ForeignKey(Workout, on_delete=CASCADE, related_name="exercises")
#     name
#     order

# class ExerciseType(models.Model):
#     name


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    name = models.CharField(max_length=100)
    notes = models.TextField(max_length=255)

    date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} -- {self.date.date()} -- {self.user}"


# class WorkoutTemplate(models.Model):
#     name
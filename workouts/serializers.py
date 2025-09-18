from rest_framework import serializers

from .models import Workout

class WorkoutSerializer(serializers.ModelSerializer):
    # exercise = ExerciseSerializer()

    class Meta:
        model = Workout
        fields = ["id", "user", "name", "notes", "date", "created", "updated", "is_deleted"]
        read_only = ["id", "user", "date", "created", "updated"]

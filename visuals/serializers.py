from rest_framework import serializers
from .models import KeyPhoto

class KeyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyPhoto
        fields = ["id", "timeline", "tpos", "weight", "s3_path", "created", "updated", "is_deleted"]
        read_only_fields = ["id", "timeline", "tpos", "created", "updated", "is_deleted"]

from rest_framework import serializers
from .models import KeyPhoto

from rest_framework import serializers
from .models import KeyPhoto


class KeyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyPhoto
        fields = ["id", "timeline", "tpos", "weight", "s3_path", "created", "is_deleted"]
        read_only_fields = ["id", "timeline", "tpos", "created", "is_deleted"]









# --- Logic for separate write and read methods ---
# class KeyPhotoWriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KeyPhoto
#         fields = ["id", "tpos", "weight"]  # timeline придёт из viewset, s3_id генерим сами
#         read_only_fields = ["id"]

# class KeyPhotoReadSerializer(serializers.ModelSerializer):
#     presigned_url = serializers.SerializerMethodField()

#     class Meta:
#         model = KeyPhoto
#         fields = ["id", "timeline", "tpos", "weight", "created", "presigned_url", "is_deleted"]
#         read_only_fields = ["id", "timeline", "created", "presigned_url", "is_deleted"]

#     def get_presigned_url(self, obj):
#         # тут будет логика генерации ссылки через boto3
#         # например: return generate_presigned_url(obj.s3_id)
#         return f"https://fake-s3/{obj.s3_id}"  # пока фейковый пример

from rest_framework import serializers
from .models import Timeline
from visuals.models import KeyPhoto
from visuals.serializers import KeyPhotoSerializer

class TimelineSerializer(serializers.ModelSerializer):
    keyphotos = KeyPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Timeline
        fields = ["id", "user", "name", "created", "updated", "is_deleted", "keyphotos"]
        read_only_fields = ["id", "user", "created", "updated", "keyphotos"]

    def validate_name(self, value):
        user = self.context['request'].user  # берем user из request
        qs = Timeline.objects.filter(user=user, name=value, is_deleted=False)
        if self.instance:  # если редактируем
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("You already have a timeline with this name.")
        return value
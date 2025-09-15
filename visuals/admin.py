from django.contrib import admin
from visuals.models import KeyPhoto, Transition

@admin.register(KeyPhoto)
class KeyPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "timeline", "tpos", "weight", "s3_path", "created", "is_deleted")

@admin.register(Transition)
class TransitionAdmin(admin.ModelAdmin):
    list_display = ("id", "timeline", "tpos", "from_keyphoto", "to_keyphoto", "s3_path", "created", "is_deleted")

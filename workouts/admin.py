from django.contrib import admin
from .models import Workout

@admin.register(Workout)
class WotrkoutAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "notes", "created", "updated", "is_deleted")
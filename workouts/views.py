from rest_framework import viewsets
from rest_framework.response import Response

from .models import Workout
from .serializers import WorkoutSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()                                     # Takes /{id}/
        if obj.is_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)

        obj.is_deleted = True
        obj.save(update_fields=["is_deleted"])
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Timeline
from .serializers import TimelineSerializer
from visuals.serializers import KeyPhotoSerializer

class TimelineViewSet(viewsets.ModelViewSet):
    serializer_class = TimelineSerializer

    def get_queryset(self):
        return Timeline.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="keyphoto")
    def add_keyphoto(self, request, pk=None):
        timeline = self.get_object()

        last = timeline.keyphotos.order_by("-tpos").first()
        next_pos = (last.tpos + 1) if last else 0

        serializer = KeyPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(timeline=timeline, tpos=next_pos)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

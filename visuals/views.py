# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from .models import KeyPhoto
from .serializers import KeyPhotoSerializer

class KeyPhotoViewSet(viewsets.ModelViewSet):
    queryset = KeyPhoto.objects.all()
    serializer_class = KeyPhotoSerializer

    # отключаем ненужные методы пока
    def list(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)






# --- Once again - more complicated unnecessary solution ---
# class KeyPhotoViewSet(viewsets.ModelViewSet):
#     queryset = KeyPhoto.objects.filter(is_deleted=False)
#     serializer_class = KeyPhotoSerializer

#     def get_queryset(self):
#         """
#         /api/keyphoto → все keyphotos пользователя
#         /api/timeline/{id}/keyphoto → только keyphotos указанного timeline
#         """
#         user = self.request.user
#         qs = super().get_queryset().filter(timeline__user=user)

#         timeline_id = self.kwargs.get("timeline_pk")  # если используешь nested routers
#         if timeline_id:
#             qs = qs.filter(timeline_id=timeline_id)

#         return qs

#     def create(self, request, *args, **kwargs):
#         timeline_id = self.kwargs.get("timeline_pk")  # берем id из URL
#         timeline = get_object_or_404(Timeline, id=timeline_id, user=request.user)

#         # вычисляем позицию
#         last_pos = timeline.keyphotos.aggregate(max_pos=models.Max("tpos"))["max_pos"] or 0
#         next_pos = last_pos + 1

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(timeline=timeline, tpos=next_pos)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)

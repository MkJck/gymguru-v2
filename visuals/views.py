from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import KeyPhoto
from .serializers import KeyPhotoSerializer


class KeyPhotoViewSet(viewsets.ModelViewSet):
    queryset = KeyPhoto.objects.all()
    serializer_class = KeyPhotoSerializer
    http_method_names = ["get", "put", "patch", "delete"]

#! redo list/get to filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()                                     # Takes /{id}/
        if obj.is_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)

        obj.is_deleted = True
        obj.save(update_fields=["is_deleted"])
        return Response(status=status.HTTP_204_NO_CONTENT)
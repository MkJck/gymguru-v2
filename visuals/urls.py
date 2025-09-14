from rest_framework.routers import DefaultRouter
from .views import KeyPhotoViewSet

router = DefaultRouter()
router.register(r'keyphoto', KeyPhotoViewSet, basename='keyphoto')

urlpatterns = router.urls

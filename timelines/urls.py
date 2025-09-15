from rest_framework.routers import DefaultRouter
from .views import TimelineViewSet

router = DefaultRouter()
router.register(r'timelines', TimelineViewSet, basename='timeline')

urlpatterns = router.urls
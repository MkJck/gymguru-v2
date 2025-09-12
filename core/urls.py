from django.urls import path
from .views import test_download
from .views import ProcessView


urlpatterns = [
    path('test-download/', test_download, name='test_download'),
    path('process/', ProcessView.as_view(), name='process'),
]
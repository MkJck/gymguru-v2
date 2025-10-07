from django.urls import path
from .views import ProcessView, task_status


urlpatterns = [
    path('process/', ProcessView.as_view(), name='process'),
    path('status/<str:task_id>/', task_status),
]
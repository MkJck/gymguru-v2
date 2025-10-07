import uuid
import boto3
from django.conf import settings
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from core.tasks import process_image_task
from celery.result import AsyncResult
from core.celery import app

@method_decorator(csrf_exempt, name="dispatch")
class ProcessView(View):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("image")
        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        bucket = settings.AWS_STORAGE_BUCKET_NAME
        input_path = f"inputs-v2/{uuid.uuid4()}.jpg"
        output_path = f"outputs-v2/{uuid.uuid4()}.jpg"

        s3 = boto3.client("s3")
        s3.upload_fileobj(file, bucket, input_path)

        # Запускаем задачу Celery
        task = process_image_task.delay(bucket, input_path, output_path)

        return JsonResponse({"task_id": task.id, "status": "queued"})
    
# def task_status(request, task_id):
#     result = AsyncResult(task_id, app=app)
#     if result.ready():
#         return JsonResponse({"state": result.state, "result": result.result})
#     return JsonResponse({"state": result.state})

def task_status(request, task_id):
    result = AsyncResult(task_id, app=app)
    
    data = {"state": result.state}
    
    if result.successful():
        # безопасно отдаём результат
        data["result"] = result.result
    elif result.failed():
        data["error"] = str(result.result)
    
    return JsonResponse(data)

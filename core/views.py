from django.shortcuts import render

from django.http import FileResponse
import os

import uuid
import boto3
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def test_download(request):
    # Берём путь к файлу (положим картинку в core/static/test.jpg)
    file_path = os.path.join(os.path.dirname(__file__), 'static', 'test.png')

    return FileResponse(open(file_path, 'rb'), content_type='image/png')



@method_decorator(csrf_exempt, name="dispatch")
class ProcessView(View):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("image")
        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # --- 1. Пути ---
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        input_path = f"inputs/{uuid.uuid4()}.jpg"
        output_path = f"outputs/{uuid.uuid4()}.jpg"

        # --- 2. Загружаем в S3 ---
        s3 = boto3.client("s3")
        s3.upload_fileobj(file, bucket, input_path)

        # --- 3. Запрос к микросервису ---
        payload = {
            "bucket": bucket,
            "input_path": input_path,
            "output_path": output_path,
        }

        try:
            resp = requests.post(settings.MICROSERVICE_URL, json=payload, timeout=300)
            resp.raise_for_status()
        except requests.RequestException as e:
            return JsonResponse({"error": f"Microservice failed: {str(e)}"}, status=502)

        # --- 4. Генерим presigned URL ---
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": output_path},
            ExpiresIn=3600
        )

        return JsonResponse({
            "status": "ok",
            "result_url": url
        })

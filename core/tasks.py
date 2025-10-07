import uuid
import time
import boto3
import requests
from django.conf import settings
from celery import shared_task

s3 = boto3.client("s3")

@shared_task(bind=True, max_retries=2)
def process_image_task(self, bucket, input_path, output_path):

    payload = {
        "bucket": bucket,
        "input_path": input_path,
        "output_path": output_path,
    }

    try:
        resp = requests.post(settings.BEN2_URL, json=payload, timeout=300)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise self.retry(exc=e, countdown=10)

    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": output_path},
        ExpiresIn=3600
    )
    return {"status": "ok", "proc_image_url": url}

# @shared_task(bind=True, max_retries=2)
# def generate_transition_task(self, bucket, photo1_path, photo2_path, transition_path):
#     payload = {
#         "bucket": bucket,
#         "photo1": photo1_path,
#         "photo2": photo2_path,
#         "transition_path": transition_path,
#     }

#     try:
#         resp = requests.post(settings.FILM_URL, json=payload, timeout=300)
#         resp.raise_for_status()
#     except requests.RequestException as e:
#         raise self.retry(exc=e, countdown=10)

#     url = s3.generate_presigned_url(
#         ClientMethod="get_object",
#         Params={"Bucket": bucket, "Key": transition_path},
#         ExpiresIn=3600
#     )
#     return {"status": "ok", "transition_url": url}
    
# @shared_task
# def test_task(x, y):
#     time.sleep(5)
#     return x + y

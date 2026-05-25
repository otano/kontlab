import os

import boto3

GARAGE_ENDPOINT = os.environ.get("GARAGE_ENDPOINT", "http://localhost:9000")
AWS_ACCESS_KEY_ID = os.environ.get("GARAGE_ACCESS_KEY", "kontlab")
AWS_SECRET_ACCESS_KEY = os.environ.get("GARAGE_SECRET_KEY", "kontlab-secret")
BUCKET_TMP = os.environ.get("GARAGE_BUCKET_TMP", "tmp-uploads")
BUCKET_PERM = os.environ.get("GARAGE_BUCKET_PERM", "documents-permanents")


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=GARAGE_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="auto",
    )


def move_to_permanent(object_key):
    client = get_s3_client()
    copy_source = {"Bucket": BUCKET_TMP, "Key": object_key}
    client.copy_object(
        CopySource=copy_source,
        Bucket=BUCKET_PERM,
        Key=object_key,
    )
    client.delete_object(Bucket=BUCKET_TMP, Key=object_key)

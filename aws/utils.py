import os.path
from uuid import uuid4

import boto3
import magic
from fastapi import UploadFile, HTTPException

import settings


KB = 1024
MB = KB * 1024

SUPPORTED_FILE_TYPES = {
    "image/png": "png",
    "image/jpeg": "jpg",
}

session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

s3 = session.resource("s3")
bucket = s3.Bucket(BUCKET_NAME)


async def upload_image(file: UploadFile, directory: str):
    contents = await file.read()
    size = len(contents)

    if not 0 < size <= 3 * MB:
        raise HTTPException(
            status_code=400,
            detail="Supported file size is up to 3 MB"
        )

    file_type = magic.from_buffer(buffer=contents, mime=True)
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {file_type}. "
                f"Supported types are {list(SUPPORTED_FILE_TYPES.values())}"
            )
        )
    file_name = os.path.join(directory, f"{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}")
    bucket.put_object(Body=contents, Key=file_name, ContentType=file_type)
    url = settings.AWS_S3_CUSTOM_DOMAIN + file_name.replace("\\", "%5C")
    return {"url": url}


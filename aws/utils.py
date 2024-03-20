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


s3 = boto3.client(
    "s3",
    aws_secret_access_key_id=settings.AWS_SECRET_ACCESS_KEY,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID
)

BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME


def upload_image(file: UploadFile, directory: str):
    if not file:
        raise HTTPException(
            status_code=400,
            detail="No file found!"
        )

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
    await s3.put_object(contents=contents, bucket=BUCKET_NAME, key=file_name)
    return {"file_name": file_name}

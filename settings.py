import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).parent

POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "https://physics-s3.s3.eu-north-1.amazonaws.com/"

PRIVATE_KEY_PATH: Path = BASE_DIR / "auth" / "certs" / "jwt-private.pem"
PUBLIC_KEY_PATH: Path = BASE_DIR / "auth" / "certs" / "jwt-public.pem"
ACCESS_TOKEN_LIFETIME_MIN = 2

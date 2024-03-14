import os

from dotenv import load_dotenv


load_dotenv()

POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")

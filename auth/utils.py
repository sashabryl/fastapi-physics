import datetime

import bcrypt
import jwt
from jwt import encode, decode

import settings
from settings import PUBLIC_KEY, PRIVATE_KEY


ALGORITHM = "RS256"


def encode_jwt(
        payload: dict,
        key: str = PRIVATE_KEY,
        algorithm: str = ALGORITHM,
        expires_min: int = settings.ACCESS_TOKEN_LIFETIME_MIN
) -> str:
    to_encode = payload.copy()
    now = datetime.datetime.utcnow()
    exp = now + datetime.timedelta(minutes=expires_min)
    to_encode.update(
        exp=exp,
        iat=now
    )
    return encode(payload=payload, key=PRIVATE_KEY, algorithm=algorithm)


def decode_jwt(
        token: str | bytes,
        key: str = PUBLIC_KEY,
        algorithm: str = ALGORITHM,
) -> dict:
    return jwt.decode(jwt=token, key=key, algorithms=[algorithm])


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)

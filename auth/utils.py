import datetime

import bcrypt
from fastapi import HTTPException
from jwt import encode, decode

import settings
from settings import PUBLIC_KEY_PATH, PRIVATE_KEY_PATH

ALGORITHM = "RS256"


def encode_jwt(
        payload: dict,
        key: str = PRIVATE_KEY_PATH.read_text(),
        algorithm: str = ALGORITHM,
        expires_sec: int = settings.ACCESS_TOKEN_LIFETIME_SEC
) -> str:
    to_encode = payload.copy()
    now = datetime.datetime.utcnow()
    exp = now + datetime.timedelta(seconds=expires_sec)
    to_encode.update(
        exp=exp,
        iat=now
    )
    return encode(payload=to_encode, key=key, algorithm=algorithm)


def decode_jwt(
        token: str | bytes,
        key: str = PUBLIC_KEY_PATH.read_text(),
        algorithm: str = ALGORITHM,
) -> dict:
    return decode(jwt=token, key=key, algorithms=[algorithm])


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def validate_password_registration(password1: str, password2: str) -> None | HTTPException:
    if not password1 == password2:
        raise HTTPException(400, "Passwords do not match.")

    if not len(password1) >= 10:
        raise HTTPException(400, "Make your password 10 or more characters long please.")

    if password1.isalpha() or password1.isdigit():
        raise HTTPException(400, "Password must contain both letters and digits.")

    if not password1.isascii():
        raise HTTPException(400, "Make sure your password consists of ascii characters only.")
    return
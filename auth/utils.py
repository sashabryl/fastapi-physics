import bcrypt
import jwt
from jwt import encode, decode
from settings import PUBLIC_KEY, PRIVATE_KEY


ALGORITHM = "RS256"


def encode_jwt(
        payload: dict,
        key: str = PRIVATE_KEY,
        algorithm: str = ALGORITHM
) -> str:
    return encode(payload=payload, key=PRIVATE_KEY, algorithm=algorithm)


def decode_jwt(
        token: str | bytes,
        key: str = PUBLIC_KEY,
        algorithm: str = ALGORITHM
) -> dict:
    return jwt.decode(jwt=token, key=key, algorithms=[algorithm])


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

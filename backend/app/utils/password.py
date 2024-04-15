from passlib import pwd
from passlib.context import CryptContext
import uuid
import time

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_password() -> str:
    return pwd.genword()


def generate_uuid(name: str) -> uuid.UUID:
    name = name + str(time.time_ns())
    return uuid.uuid5(uuid.NAMESPACE_DNS, name)

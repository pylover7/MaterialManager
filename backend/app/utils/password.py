import hashlib

from passlib import pwd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_password() -> str:
    return pwd.genword()

def md5_encrypt(input_string) -> str:
    # 创建md5对象
    md5_hash = hashlib.md5()
    # 更新哈希值
    md5_hash.update(input_string.encode('utf-8'))
    # 获取加密后的十六进制表示
    encrypted_string = md5_hash.hexdigest()
    return encrypted_string

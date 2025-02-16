import hashlib

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def md5_encrypt(input_string) -> str:
    # 创建md5对象
    md5_hash = hashlib.md5()
    # 更新哈希值
    md5_hash.update(input_string.encode('utf-8'))
    # 获取加密后的十六进制表示
    encrypted_string = md5_hash.hexdigest()
    return encrypted_string


def verify_password(plain_password: str, hashed_password: str) -> int:
    """
    验证密码
    :param plain_password: 明文密码
    :param hashed_password: 哈希密码
    :return: 0: 密码错误, 1: 密码正确, 2: 密码为初始密码
    """
    if pwd_context.verify(plain_password, hashed_password):
        if plain_password == md5_encrypt("1"):
            return 2
        else:
            return 1
    else:
        return 0


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

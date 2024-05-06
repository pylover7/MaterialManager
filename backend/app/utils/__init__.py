# coding=utf-8
# @FileName  :__init__.py
# @Time      :2024/5/5 下午7:23
# @Author    :dayezi
import base64
import time
import uuid


def base_decode(data: str) -> bytes:
    if len(data) % 3 == 1:
        data += "=="
    elif len(data) % 3 == 2:
        data += "="
    return base64.b64decode(data)


def generate_uuid(name: str) -> uuid.UUID:
    name = name + str(time.time_ns())
    return uuid.uuid5(uuid.NAMESPACE_DNS, name)

# coding=utf-8
# @FileName  :__init__.py
# @Time      :2024/5/5 下午7:23
# @Author    :dayezi
import base64


def base_decode(data: str) -> bytes:
    if len(data) % 3 == 1:
        data += "=="
    elif len(data) % 3 == 2:
        data += "="
    return base64.b64decode(data)

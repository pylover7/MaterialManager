# coding=utf-8
# @FileName  :__init__.py
# @Time      :2024/5/5 下午7:23
# @Author    :dayezi
import base64
import time
import uuid
from datetime import datetime


def base_decode(data: str) -> bytes:
    if len(data) % 3 == 1:
        data += "=="
    elif len(data) % 3 == 2:
        data += "="
    return base64.b64decode(data)


def generate_uuid(name: str) -> uuid.UUID:
    name = str(name) + str(time.time_ns())
    return uuid.uuid5(uuid.NAMESPACE_DNS, name)


def now(s: int = 1) -> str | datetime | float:
    """
    获取当前时间，形参取值
        - 0: datatime格式
        - 1: xxxx-xx-xx xx:xx:xx 字符串格式
        - 2: 浮点类型时间戳格式

    :param s: 数字

    :return: 当前日期时间
    """
    today = datetime.now()
    match s:
        case 0:
            return today
        case 1:
            return today.strftime("%Y-%m-%d %H:%M:%S")
        case 2:
            return today.timestamp()

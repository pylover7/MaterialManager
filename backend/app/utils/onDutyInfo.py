# coding=utf-8
# @FileName  :onDutyInfo.py
# @Time      :2024/4/11 下午6:13
# @Author    :dayezi
from configparser import ConfigParser
from pathlib import Path

path = Path.joinpath(Path(__file__).parent, "dutyInfo.ini")


class OnDutyInfo:
    def __init__(self):
        self.conf = ConfigParser()
        self.conf.read(filenames=path, encoding='utf-8')

    def get_glb_duty_info(self) -> dict[str, str]:
        return {
            "dutyPerson": self.conf.get("glb", "dutyPerson"),
            "dutyPersonDepart": self.conf.get("glb", "dutyPersonDepart")
        }

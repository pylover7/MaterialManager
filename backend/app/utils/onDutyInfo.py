# coding=utf-8
# @FileName  :onDutyInfo.py
# @Time      :2024/4/11 下午6:13
# @Author    :dayezi
from configparser import ConfigParser
from pathlib import Path

from app.utils import now

path = Path.joinpath(
    Path(__file__).parent.parent.parent,
    "config",
    "dutyInfo.ini")


class OnDutyInfo:
    def __init__(self):
        self.conf = ConfigParser()
        self.conf.read(filenames=path, encoding='utf-8')

    def getDutyInfo(self, area: str, metaType: str) -> dict[str, str]:
        return {
            "dutyPerson": self.conf[f"{area}.{metaType}"]["dutyPerson"],
            "dutyPersonDepart": self.conf[f"{area}.{metaType}"]["dutyPersonDepart"],
        }

    def setDutyInfo(self, area: str, metaType: str,
                    dutyPerson: str, dutyPersonDepart: str) -> None:
        self.conf[f"{area}.{metaType}"]["dutyPerson"] = dutyPerson
        self.conf[f"{area}.{metaType}"]["dutyPersonDepart"] = dutyPersonDepart
        self.conf[f"{area}.{metaType}"]["takeoverTime"] = now()
        with open(path, "w", encoding="utf-8") as f:
            self.conf.write(f)

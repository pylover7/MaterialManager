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

    async def getGlbDutyInfo(self) -> dict[str, str]:
        return {
            "dutyPerson": self.conf["glb"]["dutyPerson"],
            "dutyPersonDepart": self.conf["glb"]["dutyPersonDepart"],
        }

    async def setGlbDutyInfo(self, dutyPerson: str, dutyPersonDepart: str, takeoverTime: str) -> None:
        self.conf["glb"]["dutyPerson"] = dutyPerson
        self.conf["glb"]["dutyPersonDepart"] = dutyPersonDepart
        self.conf["glb"]["takeoverTime"] = takeoverTime
        with open(path, "w", encoding="utf-8") as f:
            self.conf.write(f)



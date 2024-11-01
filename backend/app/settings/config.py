import os
from pathlib import Path
from ruamel.yaml import YAML

from app.schemas.admin import DbInfo

config_path = Path.joinpath(Path(__file__).parent.parent.parent, "config.yml")
static_path = Path.joinpath(Path(__file__).parent.parent, "static")
yaml = YAML()


class Settings:
    DEBUG: bool = True
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        with open(config_path, "rb") as f:
            self.data = yaml.load(f)

    def _save(self):
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.data, f)

    @property
    def APP_TITLE(self) -> str:
        return self.data["app"]["title"]

    @APP_TITLE.setter
    def APP_TITLE(self, value: str):
        self.data["app"]["title"] = value

    @property
    def APP_DESCRIPTION(self):
        return self.data["app"]["description"]

    @property
    def VERSION(self):
        return self.data["app"]["version"]

    @property
    def HOST(self) -> str:
        return os.environ.get("HOST", self.data["server"]["host"])

    @property
    def PORT(self) -> int:
        return self.data["server"]["port"]

    @property
    def RELOAD(self) -> bool:
        return self.data["server"]["reload"]

    @property
    def CORS_ORIGINS(self) -> list[str]:
        return self.data["server"]["cors_origins"]

    @property
    def CORS_ALLOW_CREDENTIALS(self) -> bool:
        return self.data["server"]["cors_allow_credentials"]

    @property
    def CORS_ALLOW_METHODS(self) -> list[str]:
        return self.data["server"]["cors_allow_methods"]

    @property
    def CORS_ALLOW_HEADERS(self) -> list[str]:
        return self.data["server"]["cors_allow_headers"]

    @property
    def SECRET_KEY(self):
        return self.data["secret"]["secret_key"]

    @SECRET_KEY.setter
    def SECRET_KEY(self, value: str):
        self.data["secret"]["secret_key"] = value

    @property
    def JWT_ALGORITHM(self):
        return self.data["secret"]["jwt_algorithm"]

    @property
    def JWT_ACCESS_TOKEN_EXPIRE_MINUTES(self):
        return self.data["secret"]["jwt_access_token_expire_min"]

    @property
    def JWT_REFRESH_TOKEN_EXPIRE_MINUTES(self):
        return self.data["secret"]["jwt_refresh_token_expire_min"]

    @property
    def DATABASE_INFO(self) -> DbInfo:
        return DbInfo.parse_obj(self.data["db"])

    @property
    def DATABASE_START(self) -> str:
        return self.data["db"]["start"]

    @DATABASE_START.setter
    def DATABASE_START(self, value: str):
        self.data["db"]["start"] = value
        self._save()

    @property
    def DATABASE_HOST(self):
        return os.environ.get("DB_HOST", self.data["db"]["host"])

    @DATABASE_HOST.setter
    def DATABASE_HOST(self, value: int):
        self.data["db"]["host"] = value
        self._save()

    @property
    def DATABASE_PORT(self) -> int:
        """
        数据库端口
        """
        return self.data["db"]["port"]

    @DATABASE_PORT.setter
    def DATABASE_PORT(self, value: int):
        self.data["db"]["port"] = value
        self._save()

    @property
    def DATABASE_USERNAME(self) -> str:
        """
        数据库用户名
        """
        return os.environ.get("DB_USERNAME", self.data["db"]["username"])

    @DATABASE_USERNAME.setter
    def DATABASE_USERNAME(self, value: str):
        self.data["db"]["username"] = value
        self._save()

    @property
    def DATABASE_PASSWORD(self) -> str:
        """
        数据库密码
        """
        return os.environ.get("DB_PASSWORD", self.data["db"]["password"])

    @DATABASE_PASSWORD.setter
    def DATABASE_PASSWORD(self, value: str):
        self.data["db"]["password"] = value
        self._save()

    @property
    def DATABASE_NAME(self) -> str:
        """
        数据库名
        """
        return os.environ.get("DB_NAME", self.data["db"]["database"])

    @DATABASE_NAME.setter
    def DATABASE_NAME(self, value: str):
        self.data["db"]["database"] = value
        self._save()

    @property
    def SUPER_USER_PWD(self) -> str:
        return self.data["superUser"]["password"]

    @SUPER_USER_PWD.setter
    def SUPER_USER_PWD(self, value: str):
        self.data["superUser"]["password"] = value
        self._save()

    @property
    def SUPER_USER(self) -> dict:
        return self.data["superUser"]

    @property
    def TORTOISE_ORM(self):
        return {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.mysql",
                    "credentials": {
                        "host": self.DATABASE_HOST,
                        "port": self.DATABASE_PORT,
                        "user": self.DATABASE_USERNAME,
                        "password": self.DATABASE_PASSWORD,
                        "database": self.DATABASE_NAME
                    }
                }
            },
            "apps": {
                "models": {
                    "models": ["aerich.models", "app.models"],
                    "default_connection": "default",
                },
            },
            "use_tz": False,
            "timezone": "Asia/Shanghai",
        }

    @property
    def APP_LOG_CONFIG(self) -> dict:
        return self.data["log"]

    @property
    def STATIC_PATH(self) -> Path:
        return static_path


settings = Settings()

if __name__ == '__main__':
    settings.DATABASE_START = "mysql"
    print(settings.DATABASE_START)

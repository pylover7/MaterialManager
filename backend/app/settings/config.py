import os
import typing

from dotenv import load_dotenv
from pathlib import Path

from pydantic_settings import BaseSettings


env_path = Path.joinpath(Path(__file__).parent.parent.parent, ".env")
load_dotenv(dotenv_path=env_path, verbose=True, override=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    VERSION: str = os.getenv("VERSION")
    APP_TITLE: str = os.getenv("APP_TITLE")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION")
    
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))
    RELOAD: bool = eval(os.getenv("RELOAD"))

    CORS_ORIGINS: typing.List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: typing.List = ["*"]
    CORS_ALLOW_HEADERS: typing.List = ["*"]

    DEBUG: bool = True

    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "app/logs")
    SECRET_KEY: str = os.getenv("SECRET_KEY")  # openssl rand -hex 32
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")  # HS256
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_MINUTES"))  # 60 minutes
    TORTOISE_ORM: dict = {
        "connections": {
            # "sqlite": {
            #     "engine": "tortoise.backends.sqlite",
            #     "credentials": {"file_path": f"{BASE_DIR}/db.sqlite3"},
            # },
            "mysql": {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "host": os.getenv("DB_HOST"),
                    "port": os.getenv("DB_PORT"),
                    "user": os.getenv("DB_USERNAME"),
                    "password": os.getenv("DB_PASSWORD"),
                    "database": os.getenv("DB_NAME"),
                }
            }
        },
        "apps": {
            "models": {
                "models": ["app.models"],
                "default_connection": "mysql",
            },
        },
        "use_tz": False,
        "timezone": "Asia/Shanghai",
    }
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    
    APP_LOG_CONFIG: object = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
      "default": {
        "()": "uvicorn.logging.DefaultFormatter",
        "fmt": "%(levelprefix)s %(message)s",
        "use_colors": "null"
      },
      "access": {
        "()": "uvicorn.logging.AccessFormatter",
        "fmt": "%(asctime)s - %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"
      }
    },
    "handlers": {
      "default": {
        "formatter": "default",
        "class": "logging.StreamHandler",
        "stream": "ext://sys.stderr"
      },
      "access": {
        "formatter": "access",
        "class": "logging.StreamHandler",
        "stream": "ext://sys.stdout"
      }
    },
    "loggers": {
      "uvicorn": {
        "handlers": [
          "default"
        ],
        "level": "INFO"
      },
      "uvicorn.error": {
        "level": "INFO"
      },
      "uvicorn.access": {
        "handlers": [
          "access"
        ],
        "level": "INFO",
        "propagate": False
      }
    }
  }


settings = Settings()

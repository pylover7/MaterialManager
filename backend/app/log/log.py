import sys

from loguru import logger as loguru_logger

from app.settings import settings


class Logger:

    def __init__(self):
        self.logger = loguru_logger
        self.logger.remove()
        self.logger.add(
            sink=sys.stderr,
            level=settings.DEBUG,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> |"
                   " <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
        )

    def get_logger(self):
        return self.logger


logger = Logger().get_logger()

if __name__ == '__main__':
    logger.info("nihao")

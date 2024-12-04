from pathlib import Path
import sys

from loguru import logger as loguru_logger

class Logger:

    def __init__(self):
        self.logger = loguru_logger
        loginLogs = Path(__file__).parent.parent.parent.joinpath("logs", "login.log")
        systemLogs = Path(__file__).parent.parent.parent.joinpath("logs", "system.log")
        self.logger.remove()
        self.logger.add(
            sink=sys.stderr,
            level="DEBUG",
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> |"
                   " <level>Logger: {extra[name]}</level> | <level>{message}</level>"
        )
        self.logger.add(
            sink=loginLogs,
            level="DEBUG",
            rotation="10 MB",
            encoding="utf-8",
            retention="10 days",
            compression="zip",
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {extra[ip]}  | <level>{message}</level>",
            filter=lambda record: record["extra"].get("name") == "login"
        )
        self.logger.add(
            sink=systemLogs,
            level="DEBUG",
            rotation="10 MB",
            encoding="utf-8",
            retention="10 days",
            compression="zip",
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            filter=lambda record: record["extra"].get("name") == "system"
        )

    def defaultLogger(self):
        return self.logger.bind(name="system")

    def loginLogger(self):
        return self.logger.bind(name="login")


logger = Logger().defaultLogger()
loginLogger = Logger().loginLogger()

if __name__ == '__main__':
    loginLogger.success("123", ip="12.0.0.1")
    loginLogger.error("zhangsan", ip="127.0.0.1")
    logger.info("123")

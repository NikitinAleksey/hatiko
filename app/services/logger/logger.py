import logging

__all__ = ["AppLogger"]


class AppLogger:
    def __init__(
            self, name: str,
            log_file_name: str = None,
            level=logging.DEBUG
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if log_file_name:
            self.logger.addHandler(console_handler)
            file_handler = logging.FileHandler(log_file_name)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str):
        """Логирование отладочных сообщений."""
        self.logger.debug(message)

    def info(self, message: str):
        """Логирование информационных сообщений."""
        self.logger.info(message)

    def warning(self, message: str):
        """Логирование предупреждений."""
        self.logger.warning(message)

    def error(self, message: str):
        """Логирование ошибок."""
        self.logger.error(message)

    def critical(self, message: str):
        """Логирование критических ошибок."""
        self.logger.critical(message)

    def set_level(self, level: int):
        """Изменить уровень логирования для этого логгера."""
        self.logger.setLevel(level)

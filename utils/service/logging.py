import logging


class LoggerService:
    logger = None

    @classmethod
    def init_logger(cls):
        cls.logger = logging.getLogger(f"{cls.__module__}:{cls.__name__}")

    @classmethod
    def check_logger(cls):
        if cls.logger is None:
            cls.init_logger()

    @classmethod
    def exception(cls, msg, **kwargs):
        kwargs.pop('exc_info', None)
        cls.warning(msg, exc_info=True, **kwargs)

    @classmethod
    def warning(cls, msg,  **kwargs):
        cls.check_logger()
        cls.logger.warning(msg,  **kwargs)

    @classmethod
    def error(cls, msg,  **kwargs):
        cls.check_logger()
        cls.logger.error(msg,  **kwargs)

    @classmethod
    def info(cls, msg, **kwargs):
        cls.check_logger()
        cls.logger.info(msg, **kwargs)

    @classmethod
    def debug(cls, msg,  **kwargs):
        cls.check_logger()
        cls.logger.debug(msg,  **kwargs)

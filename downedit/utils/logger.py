import logging
import time

from rich.logging import RichHandler
from rich.traceback import install

from .singleton import Singleton

install()

class Formatter(logging.Formatter):
    msg_color = {
        "DEBUG"     : "cyan",
        "INFO"      : "green",
        "WARNING"   : "yellow",
        "ERROR"     : "red",
        "CRITICAL"  : "bold red",
        "FILE"      : "magenta",
    }

    def __init__(self, fmt="{message}", style='{', datefmt="[%X]"):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record):
        """
        Format the message with color based on the log level
        """
        # Retrieve the original message
        message = record.getMessage()
        # color = self.msg_color.get(record.levelname, 'white')
        # message = f"[{color}]{message}[/]"
        record.msg = message
        return super().format(record)
    

class Logger(metaclass=Singleton):
    def __init__(self):
        # Prevent re-initialization of the logger
        if hasattr(self, '_ready'):
            return

        self.prime_logger = logging.getLogger("DownEdit")
        self.prime_logger.setLevel(logging.DEBUG)
        self._ready = True

    def config_log(self, log_level=logging.DEBUG):
        """
        Set new log level and configure 
        """
        self.prime_logger.handlers.clear()
        self.prime_logger.setLevel(log_level)
        
        console_handler = RichHandler(
            show_time=True,
            show_path=False,
            markup=True,
            rich_tracebacks=True,
            omit_repeated_times=False
        )
        console_handler.setFormatter(Formatter())
        self.prime_logger.addHandler(console_handler)

    def close(self):
        # Properly close and remove all handlers
        for handler in self.prime_logger.handlers:
            handler.close()
            self.prime_logger.removeHandler(handler)
        self.prime_logger.handlers.clear()
        # Ensure all logs are processed before exit
        time.sleep(1)


# Adding custom log level method
FILE_LEVEL_NUM = 25
logging.addLevelName(FILE_LEVEL_NUM, "FILE")

def file(self, message, *args, **kwargs):
    if self.isEnabledFor(FILE_LEVEL_NUM):
        self._log(FILE_LEVEL_NUM, message, args, **kwargs)

logging.Logger.file = file


def init_logging():
    logger = logging.getLogger("DownEdit")
    if not logger.handlers:
        log_control = Logger()
        log_control.config_log(log_level=logging.DEBUG)
    return logger


# Initialize the logger
logger = init_logging()
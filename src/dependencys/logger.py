import logging

from config import SETTINGS


logging.basicConfig(level=SETTINGS.LOGGER_LVL)
logger = logging.getLogger(__name__)


def get_routs_logger() -> logging.Logger:
    return logger

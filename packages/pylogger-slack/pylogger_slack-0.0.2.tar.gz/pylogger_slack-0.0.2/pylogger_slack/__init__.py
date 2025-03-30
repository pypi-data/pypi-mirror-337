# pylogger_slack/__init__.py


from pylogger_slack._config import Configuration
from pylogger_slack.logger import LoggerFormatter, LoggerInitializer
from pylogger_slack.slack import SlackNotification
import logging

__version__ = "0.1.0"
CONFIG = Configuration().config


LOGGER = logging.getLogger(__name__)
initializer = LoggerInitializer()
initializer(logger=LOGGER)

SLACK = SlackNotification(webhook=None, dev=True)

__all__ = ["LOGGER", "SLACK", "CONFIG", "__version__"]
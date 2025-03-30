# pylogger_slack/logger.py
import http.client
import logging
import logging.config
from functools import partial
from typing import Optional
import yaml
import json
import warnings
import ecs_logging

class LoggerFormatter(logging.Formatter):
    def __init__(self, format, datefmt=None, extra=None, exclude_fields=None):
        super().__init__(fmt=format, datefmt=datefmt)
        self.default_extra = extra or {}
        self.exclude_fields = exclude_fields or []

    def format(self, record):
        from pylogger_slack import CONFIG
        format_type = CONFIG.get("format_type", "default")

        # Base formatted message
        base_message = super().format(record)

        # Handle extra data
        extra = record.extra if hasattr(record, "extra") else {}
        combined_extra = {**self.default_extra, **extra}
        filtered_extra = {k: v for k, v in combined_extra.items() if k not in self.exclude_fields}

        if format_type == "yaml":
            return yaml.dump({"log": base_message, "extra": filtered_extra})
        elif format_type == "json":
            return json.dumps({"log": base_message, "extra": filtered_extra})
        return base_message

class LoggerInitializer:
    def __call__(self, logger: logging.Logger, name: Optional[str] = None):
        from pylogger_slack import CONFIG
        self.config = CONFIG
        
        logger.name = name if name else logger.name if logger.name != "__main__" else __name__
        self._apply_config(logger)
        
        http.client.HTTPConnection.debuglevel = 1
        http.client.print = partial(self._print_to_log, logger)

    def _apply_config(self, logger: logging.Logger):
        try:
            logging.config.dictConfig(self.config)
        except Exception as e:
            warnings.warn(f"Failed to apply logger config: {e}")

    def _print_to_log(self, logger: logging.Logger, *args, **kwargs):
        k = ".".join(str(arg) for arg in args[:-1])
        v = str(args[-1])
        extra = ecs_logging._utils.de_dot(k, v)
        extra.update(kwargs)
        extra.update({"type": "access-log"})
        logger.debug("HTTP log", extra=extra)
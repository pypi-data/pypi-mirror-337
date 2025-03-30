# pylogger_slack

A Python logging utility with Slack notification support, built for flexibility and ease of use. `pylogger_slack` provides a customizable logger with structured output options (plain text, JSON, YAML) and integrates with Slack for notifications. It’s designed to work out of the box with sensible defaults while allowing deep customization via a TOML configuration file.

**Support my development**

<a href="https://www.buymeacoffee.com/i_binay" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 117px !important;" ></a>

## Installation

Install `pylogger_slack` via pip (assuming it’s published to PyPI, or install locally):

```bash
pip install pylogger_slack
```

**Dependencies**:
- `ecs-logging` (for ECS formatting)
- `pyyaml` (for YAML output)
- `slack-sdk` (optional, for Slack notifications)


## Quick Start

Here’s a basic example to get started:

```python
# example.py
from pylogger_slack import LOGGER, SLACK

LOGGER.info("This is an info message.")
LOGGER.info("Tagged message", extra={"tag": "v1.0"})
SLACK.notify("Something happened!")
```

Run it:
```bash
python example.py
```

**Output** (default config, with format_type=default):
```
2025-03-29 12:34:56 - __main__ - INFO - This is an info message.
2025-03-29 12:34:56 - __main__ - INFO - Tagged message
Slack notification (dev mode): Something happened!
```

## Configuration

`pylogger_slack` uses a default configuration but can be customized via a `pylogger_slack.toml` file in your project root level.


### Customizing with `pylogger_slack.toml`

```toml
# pylogger_slack.toml
[formatters.default]
format = "%(levelname)s - %(message)s"
extra = { "app" = "my_app" }
exclude_fields = ["user_id", "secret"]
format_type = "json"
```

Run `example.py` with this file in the same directory:
```json
{"log": "INFO - This is an info message.", "extra": {"app": "my_app"}}
{"log": "INFO - Tagged message", "extra": {"app": "my_app", "tag": "v1.0"}}
```

### `pylogger_slack.toml` Syntax
Below is the complete syntax with examples and explanations.

```toml

disable_existing_loggers = false # Whether to disable other loggers (true/false)
slack_webhook_url = "https://hooks.slack.com/services/T00" # Webhook
dev = false   # False to send real Slack notifications

# General settings
env = "production"  # Environment name
format_type = "json"  # Output type: "default" (plain), "json", "yaml"

# Formatter configuration
[formatters.default]    # Name can be changed (e.g., "custom")
"()" = "pylogger_slack.logger.LoggerFormatter"  # Class to instantiate (optional, default provided)
format = "%(asctime)s [%(levelname)s] %(message)s"  # Log format string
datefmt = "%H:%M:%S"           # Date/time format (optional)
extra = { "app" = "my_app", "version" = "1.0" }  # Default extra fields
exclude_fields = ["user_id", "secret"]  # Fields to exclude from structured output

# Additional formatter example
[formatters.detailed]
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s - tag:%(tag)s"
extra = { "service" = "api" }
exclude_fields = ["log.original"]

# Handler configuration
[handlers.console]
class = "logging.StreamHandler"  # Handler class
level = "INFO"                   # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
formatter = "default"            # Reference to a formatter name
stream = "ext://sys.stdout"      # Output stream (ext://sys.stdout or ext://sys.stderr)

[handlers.file]
class = "logging.FileHandler"
level = "WARNING"
formatter = "detailed"
filename = "app.log"             # File to log to

# Root logger configuration
[root]
level = "DEBUG"                  # Root log level
handlers = ["console", "file"]   # List of handler names
```

### Custom Config in Code
Override config programmatically:
```python
from pylogger_slack import LOGGER, SLACK, CONFIG, LoggerInitializer

CONFIG["format_type"] = "yaml"
CONFIG["formatters"]["default"]["extra"] = {"app": "web"}
CONFIG["root"]["level"] = "DEBUG"
initializer = LoggerInitializer()
initializer(LOGGER)  # Reapply config

LOGGER.debug("Now visible!")
SLACK.notify("Test notification")
```

**Output:**
```yaml
log: '2025-03-29 12:34:56 - __main__ - DEBUG - Now visible!'
extra:
  app: web
```

**Output:**
```
DEBUG - Debug message - app:my_app
```

## Advanced Features

### Excluding Fields
Exclude sensitive data:
```toml
[formatters.default]
exclude_fields = ["password", "token"]
format_type = "json"
```
```python
LOGGER.info("Login", extra={"password": "secret", "user": "alice"})
```
```json
{"log": "INFO - Login", "extra": {"user": "alice"}}
```

### Multiple Handlers
Log to console and file:
```toml
[handlers.console]
class = "logging.StreamHandler"
level = "INFO"
formatter = "default"

[handlers.file]
class = "logging.FileHandler"
level = "ERROR"
formatter = "default"
filename = "errors.log"

[root]
handlers = ["console", "file"]
```
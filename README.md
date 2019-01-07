[![](https://img.shields.io/pypi/v/sc2monitor.svg)](https://pypi.org/project/sc2monitor/)

# discord-logger
A Python logger to send information to Discord Webhooks.

## Installation
Install this package via `pip` by executing `pip install discordlogger`

## Usage

### Basic Usage

```python
import logging

from discordlogger import DiscordFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
h = DiscordHandler(webhook_url=URL)
h.setLevel(logging.INFO)
logger.addHandler(h)

logger.info('Hello World')
```

### Advanced Formating

```python
import logging

from discordlogger import DiscordFormatter, DiscordHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
h = DiscordHandler(webhook_url=URL)
h.formatter = DiscordFormatter()
logger.addHandler(h)

logger.info('Hello World')
logger.warning('Warning!')
try:
    print(data['hello'])
except Exception:
    logger.exception('Exception!')
logger.critical('Emergency here!')
```

### Filtering

```python
import logging

from discordlogger import DiscordFormatter, DiscordLogFilter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
h = DiscordHandler(webhook_url=URL)
h.addFilter(DiscordLogFilter())
logger.addHandler(h)

# Now this doesn't activate the discord webhook
logger.info("Hello World")

# Whereas this does
logger.info("Hello World", extra={'notify_discord': True})
```

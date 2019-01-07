import logging

from discordlogger import DiscordFormatter, DiscordHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
h = DiscordHandler(
    webhook_url=URL)
h.setLevel(logging.INFO)
h.formatter = DiscordFormatter()
logger.addHandler(h)
logger.info("Hello World")
logger.warning('Warning!')
data = dict()
try:
    print(data['hello'])
except Exception:
    logger.exception('message')

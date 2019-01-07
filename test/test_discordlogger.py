import logging

from discordlogger import DiscordHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
h = DiscordHandler(
    webhook_url=URL)
h.setLevel(logging.INFO)
logger.addHandler(h)
logger.info("Hello World")

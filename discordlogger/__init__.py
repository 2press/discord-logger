# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

import logging
import traceback
from datetime import datetime
from threading import Semaphore
from time import sleep

import requests

__version__ = '0.0.2'


class DiscordHandler(logging.Handler):
    """Logging handler to post to Slack to the webhook URL"""

    def __init__(self, webhook_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.webhook_url = webhook_url
        self.formatter = SimpleDiscordFormatter()
        self._lock = Semaphore(5)

    def emit(self, record):
        """Submit the record with a POST request"""
        headers = {'User-agent': f'discord-logger {__version__}'}
        json_data = self.format(record)
        max_retries = 3
        for retries in range(max_retries - 1):
            with self._lock:
                r = requests.post(self.webhook_url,
                                  json=json_data, headers=headers)
            if r.status_code == 429:
                retry_after = int(r.headers.get('Retry-After', 500)) / 100.0
                sleep(retry_after)
                continue
            elif r.status_code < 400:
                break
            else:
                continue
        try:
            r.raise_for_status()
        except Exception:
            self.handleError(record)


class DiscordLogFilter(logging.Filter):
    """
    Logging filter to decide when logging to Slack is requested, using
    the `extra` kwargs:

        `logger.info("...", extra={'notify_discord': True})`
    """

    def filter(self, record):
        return getattr(record, 'notify_discord', False)


class SimpleDiscordFormatter(logging.Formatter):
    """Basic formatter without styling"""

    def format(self, record):
        return {'content': record.getMessage()}


class DiscordFormatter(logging.Formatter):
    def format(self, record):
        """
        Format message content, timestamp when it was logged and a
        coloured border depending on the severity of the message
        """
        msg = record.getMessage()
        exc = record.__dict__['exc_info']
        if exc:
            msg = msg + '\n```{}```'.format(traceback.format_exc())
        embed = dict()
        embed["description"] = msg
        embed['timestamp'] = datetime.utcnow().isoformat()
        embed['author'] = {'name': '{}@{}'.format(
            record.name, record.filename)}
        try:
            colors = {
                'DEBUG': 810979,
                'INFO': 1756445,
                'WARNING': 15633170,
                'ERROR': 16731648,
                'CRITICAL': 16711680,
            }
            embed['color'] = colors[record.levelname]
        except KeyError:
            pass
        return {'embeds': [embed]}

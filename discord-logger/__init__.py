# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

import logging

import requests

__version__ = '0.0.1'


class DiscordHandler(logging.Handler):
    """Logging handler to post to Slack to the webhook URL"""

    def __init__(self, webhook_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.webhook_url = webhook_url
        self.formatter = SimpleSlackFormatter()

    def emit(self, record):
        """Submit the record with a POST request"""
        try:
            json_data = self.format(record)
            r = requests.post(self.webhook_url, json=json_data)
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
        return {'content': record.getMessage()}
        ret = {
            'ts': record.created,
            'text': record.getMessage(),
        }
        try:
            loglevel_colour = {
                'INFO': 'good',
                'WARNING': 'warning',
                'ERROR': '#E91E63',
                'CRITICAL': 'danger',
            }
            ret['color'] = loglevel_colour[record.levelname]
        except KeyError:
            pass
        return {'attachments': [ret]}

from datetime import datetime
from time import strptime
import re

__author__ = 'Mark Schmale <masch@masch.it>'


class Message():
    def __init__(self, msgid, timestamp, sender, msg, channel=""):
        self.received = datetime.utcnow()
        self.time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        self.sender = sender.replace('_', ' ')
        self.channel = channel
        self.message = msg

    def __str__(self):
        return "[{time}|{received}] [{sender} @ {channel}] : {message}".format(
            time=self.time,
            received=self.received,
            sender=self.sender,
            channel=self.channel,
            message=self.message
        )




# coding=utf-8
from TelegramConnection import TelegramConnection
from Message import Message
import re

class TelegramClient(TelegramConnection):

    def __init__(self, host, port):
        TelegramConnection.__init__(self, host, port)
        self.re_grp_msg = None
        self.re_msg = None
        self.compileRe()

    def compileRe(self):
        self.re_grp_msg = re.compile(r"(?P<msgid>\d+)\s+\[(?P<time>.*)\]\s+(?P<channel>.*) @ (?P<sender>.*) [»>]+ (?P<msg>.*)$")
        self.re_msg = re.compile(r"(?P<msgid>\d+)\s+\[(?P<time>.*)\]\s+(?P<sender>.*) [»>]+ (?P<msg>.*)$")

    def start_main_session(self):
        self.send("main_session\n")

    def msg(self, channel, message):
        self.send("msg " + channel.replace(" ", "_") + " " + message)

    def handle_answer(self, msg):
        """
        :type msg str
        """
        groups = self.re_msg.match(msg)
        if groups:
            mes = Message(
                groups.group("msgid"),
                groups.group("time"),
                groups.group("sender"),
                groups.group("msg")
            )
        groups = self.re_grp_msg.match(msg)
        if groups:
            mes = Message(
                groups.group("msgid"),
                groups.group("time"),
                groups.group("sender"),
                groups.group("msg"),
                groups.group("channel")
            )

        if mes:
            self.on_message(mes)
        else:
            print "<<< " + msg

    def on_message(self, message):
        """
        :param message:
        :type message Message
        :return:
        """

        print message



print "starting..."
client = TelegramClient("localhost", 9012)
client.start_main_session()
client.loop()
print "done.."



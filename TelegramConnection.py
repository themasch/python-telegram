# coding=utf-8
import asyncore
import socket
import re

from Message import Message


class TelegramConnection(asyncore.dispatcher):

    def __init__(self, host="localhost", port=9012):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = ''
        self._matcher = None
        self.re_grp_msg = None
        self.re_msg = None
        self.compileRe()
        print "waiting for connection.."

    def compileRe(self):
        self._matcher = re.compile(r"^\s*ANSWER (?P<length>\d+)\s+(?P<data>.*)")
        self.re_grp_msg = re.compile(r"(?P<msgid>\d+)\s+\[(?P<time>.*)\s+\+0200\]\s+(?P<channel>.*) @ (?P<sender>.*) [»>]+ (?P<msg>.*)$")
        self.re_msg = re.compile(r"(?P<msgid>\d+)\s+\[(?P<time>.*)\s+\+0200\]\s+(?P<sender>.*) [»>]+ (?P<msg>.*)$")

    def start_main_session(self):
        self.send("main_session\n")

    def msg(self, channel, message):
        self.send("msg " + channel.replace(" ", "_") + " " + message + "\n")

    def send(self, data):
        if isinstance(self.buffer, basestring):
            self.buffer = self.buffer + data
        else:
            self.buffer = data

    def handle_answer(self, msg):
        """
        :type msg str
        """
        mes = False
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

    def handle_connect(self):
        print "should be connected"
        pass

    def handle_close(self):
        print "closing socket to tg: "
        self.close()
        print "closed"

    def handle_read(self):
        msg = self.recv(8192)
        #print ">> " + msg
        self.parse_message(msg)

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = asyncore.dispatcher.send(self, self.buffer)
        print "sending: " + self.buffer[:sent]
        self.buffer = self.buffer[sent:]

    def parse_message(self, msg):
        result = self._matcher.match(msg)
        if result:
            sLenght = result.group('length')
            data = result.group('data')
            start = len('ANSWER ' + sLenght) + 1
            length = int(sLenght)
            message = data[0:length]
            self.handle_answer(message)
            self.parse_message(data[length:])

    def loop(self):
        asyncore.loop()

    def on_message(self, message):
        """
        :param message:
        :type message Message
        :return:
        """

        print message

# coding=utf-8
import socket
import re
import select
import errno
import sys

from Message import Message


class TelegramConnection():

    def __init__(self, host="localhost", port=9012):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(None)
        err = self.socket.connect_ex((host, port))
        if err:
            print errno.errorcode[err]

        self.buffer = ''
        self._matcher = None
        self.re_grp_msg = None
        self.re_msg = None
        self.compileRe()
        self.running = True

        self.msg_callbacks = []

    def compileRe(self):
        self._matcher = re.compile(r"^\s*ANSWER (?P<length>\d+)\s+(?P<data>.*)")
        self.re_grp_msg = re.compile(r"(?P<msgid>\d+)\s+\[(?P<time>.*)\s+\+\d+\]\s+(?P<channel>.*) @ (?P<sender>.*) [»>]+ (?P<msg>.*)$")
        self.re_msg = re.compile(r"(?P<msgid>\d+)\s+\[(?P<time>.*)\s+\+\d+\]\s+(?P<sender>.*) [»>]+ (?P<msg>.*)$")

    def start_main_session(self):
        self.send("main_session\n")

    def msg(self, channel, message):
        self.send("msg " + channel.replace(" ", "_") + " " + message + "\n")

    def send(self, data):
        self.socket.sendall(data)

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
            self.handle_message(mes)
        else:
            print "<<< " + msg

    def close(self):
        print "close().."
        self.running = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print "socket.close()"

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
        while self.running:
            try:
                data = self.socket.recv(8192)
                print "got data.."
                if data:
                    self.parse_message(data)
                else:
                    print >>sys.stderr, 'closing: ', self.socket.getpeername()
                    self.socket.close()
                    self.running = False
            except socket.error as err:
                if err.errno != 9:
                    print "socket error: ({0}) {1}".format(err.errno, err.strerror)

    def on_message(self, cb):
        self.msg_callbacks.append(cb)

    def handle_message(self, message):
        for cb in self.msg_callbacks:
            cb(message)

        print message

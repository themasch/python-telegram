# coding=utf-8
import socket
import re
import select
import errno

from Message import Message


class TelegramConnection():

    def __init__(self, host="localhost", port=9012):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
        err = self.socket.connect_ex((host, port))
        if err:
            print errno.errorcode[err]

        self.buffer = ''
        self._matcher = None
        self.re_grp_msg = None
        self.re_msg = None
        self.compileRe()
        print "waiting for connection.."
        self.running = True

    def compileRe(self):
        self._matcher = re.compile(r"^\s*ANSWER (?P<length>\d+)\s+(?P<data>.*)")
        self.re_grp_msg = re.compile(r"(?P<msgid>\d+)\s+\[(?P<time>.*)\s+\+0200\]\s+(?P<channel>.*) @ (?P<sender>.*) [»>]+ (?P<msg>.*)$")
        self.re_msg = re.compile(r"(?P<msgid>\d+)\s+\[(?P<time>.*)\s+\+0200\]\s+(?P<sender>.*) [»>]+ (?P<msg>.*)$")

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
            self.on_message(mes)
        else:
            print "<<< " + msg

    def close(self):
        self.socket.close()

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
            sockets = [ self.socket ]
            print "waiting for event..."
            readable, writable, errored = select.select(sockets, [ ], sockets)

            for sock in readable:
                data = sock.recv(8192)
                if data:
                    self.parse_message(data)
                else:
                    sock.close()
                    self.running = Falses

            for sock in errored:
                print >>sys.stderr, 'handling exceptional condition for', sock.getpeername()
                sock.close()



    def on_message(self, message):
        """
        :param message:
        :type message Message
        :return:
        """

        print message

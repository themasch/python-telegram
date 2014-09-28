from TelegramConnection import TelegramConnection
import re

class TelegramClient(TelegramConnection):

    def __init__(self, host, port):
        TelegramConnection.__init__(self, host, port)
        self.compileRe()

    def compileRe(self):
        self.re_msg = re.compile(r"(?P<msgid>\d+)\s+\[(.*)\]\s+")

    def start_main_session(self):
        self.send("main_session\n")

    def msg(self, channel, message):
        self.send("msg " + channel.replace(" ", "_") + " " + message)

    def handle_answer(self, msg):
        pass


print "starting..."
client = TelegramClient("localhost", 9012)
client.start_main_session()
client.loop()
print "done.."



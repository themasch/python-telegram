from TelegramConnection import TelegramConnection

class TelegramClient(TelegramConnection):

    def __init__(self, host, port):
        TelegramConnection.__init__(self, host, port)

    def start_main_session(self):
        self.send("main_session\n")

    def msg(self, channel, message):
        self.send("msg " + channel.replace(" ", "_") + " " + message)

    def handle_answer(self, msg):


print "starting..."
client = TelegramClient("localhost", 9012)
client.start_main_session()
client.loop()
print "done.."



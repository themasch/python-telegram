import asyncore, socket, re

class TelegramConnection(asyncore.dispatcher):

    def __init__(self, host="localhost", port=9012):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        #self.buffer = 'main_session\n'
        self._matcher = re.compile(r"^\s*ANSWER (?P<length>\d+)\s+(?P<data>.*)")

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        msg = self.recv(8192)
        #print ">> " + msg
        self.parse_message(msg)

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def parse_message(self, msg):
        result = self._matcher.match(msg)
        if result:
            sLenght = result.group('length')
            data    = result.group('data')
            start   = len('ANSWER ' + sLenght) + 1
            length  = int(sLenght)
            message = data[0:length]
            self.handle_answer(message)
            self.parse_message(data[length:])
        #else:
        #    print "parsing done.."
#        print ">>msg id: " + result.group('id')
#        print ">>data\n" + "-----------------\n" + result.group('data') + "\n------------------\n"

    def handle_answer(self, data):
        print ">> got answer " + data

    def loop(self):
        asyncore.loop()

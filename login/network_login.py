import socket


class NetworkLogin:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5566
        self.addr = (self.server, self.port)
        self.respond = self.connect()

    def getRespond(self):
        return self.respond

    def connect(self):
        try:
            self.client.connect(self.addr) # Connection
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
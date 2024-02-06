import socket
import pickle


class Network:

    def __init__(self, ip, port, uuid):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.uuid = uuid
        self.playerdata = self.connect(uuid)


    def get_player(self):
        print("first")
        print(self.playerdata)
        return self.playerdata

    # Fist connection Return Fist message
    def connect(self, uuid):
        try:
            self.client.connect(self.addr)
            self.client.send(str.encode(uuid))
            return pickle.loads(self.client.recv(2048))  # Recuperation des players data
        except:
            pass

    def rcv_obj(self):
        nb_players = pickle.loads(self.client.recv(2048))  # pickle.loads() recompose l'object
        print(nb_players)
        self.client.send(str.encode("ok"))
        return nb_players

    def rcv_str(self):
        received_str = self.client.recv(2048).decode("utf-8")
        print(received_str)
        self.client.send(str.encode("ok"))
        return received_str

    # Send information and receve respond
    def send_obj(self, data):
        try:
            self.client.send(pickle.dumps(data))   # pickle.dump decompose l'object en binaire
            self.client.recv(2048).decode()  # Wait
        except socket.error as e:
            print(e)

    def send_str(self, data):
        try:
            self.client.send(str.encode(data))
            self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def close(self): self.client.close()

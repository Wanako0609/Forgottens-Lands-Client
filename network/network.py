import socket
import pickle


class Network:

    def __init__(self, ip, port, uuid):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.uuid = uuid
        self.player_data = self.connect(uuid)

    def recv(self): return self.client.recv(1024)

    def get_player(self): return self.player_data

    def send(self, label: str, data):
        labeled_data = {"label": label, "data": data}
        print("data send", labeled_data)
        self.client.send(pickle.dumps(labeled_data))

    # Fist connection Return Fist message
    def connect(self, uuid):
        try:
            self.client.connect(self.addr)
            #self.client.send(str.encode(uuid))
            self.send(label="connection", data=uuid)
            data = pickle.loads(self.client.recv(2048))  # Recuperation des players data
            if data["label"] == "connection":
                player_data = data["data"]
                return player_data
            str_r = "Mauvais message reçu", data["label"]
            assert False, str_r

        except socket.error as se:
            assert False, f"Socket error: {se}"
            # Gérer les erreurs spécifiques ici
        except pickle.PickleError as pe:
            assert False,f"Pickle error: {pe}"
            # Gérer les erreurs de désérialisation spécifiques ici
        except Exception as e:
            assert False,f"Unexpected error: {e}"
            # Gérer d'autres erreurs non prévues ici

    def close(self):
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()


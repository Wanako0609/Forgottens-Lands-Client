import socket
import pickle
import threading
import time
from queue import Queue


class Network:

    def __init__(self, ip, port, uuid):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.uuid = uuid
        self.player_data = self.connect(uuid)

        # Création de threads pour l'envoi et la réception
        self.recv_thread = threading.Thread(target=self.recv_thread_method)

        self.running = True

        # File partagée entre les threads de réception et le thread principal
        self.message_queue = Queue()

    def get_player(self): return self.player_data

    def start_threads(self):
        # Démarrer les threads d'envoi et de réception
        self.recv_thread.start()

    def send(self, label: str, data):
        labeled_data = {"label": label, "data": data}
        print("data send", labeled_data)
        self.client.send(pickle.dumps(labeled_data))

    def recv_thread_method(self):
        while self.running:
            try:
                data_recv = self.client.recv(2048)
                #print(data_recv)

                data = pickle.loads(data_recv)  # pickle.loads() recompose l'object

                # Mettez les données dans la file pour que le thread principal les récupère
                self.message_queue.put(data)

            except socket.error as e:
                print("error")
                print(e)
                self.close()

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
            print(f"Socket error: {se}")
            # Gérer les erreurs spécifiques ici
        except pickle.PickleError as pe:
            print(f"Pickle error: {pe}")
            # Gérer les erreurs de désérialisation spécifiques ici
        except Exception as e:
            print(f"Unexpected error: {e}")
            # Gérer d'autres erreurs non prévues ici

    def close(self):
        # Arrêter les threads avant de fermer la connexion
        self.running = False
        self.recv_thread.join()
        self.client.close()


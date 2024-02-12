import time
from queue import Queue
import pickle
import socket
import threading

from network.network import Network


class ThreadManager:

    def __init__(self, n: Network):

        self.running = True
        self.client = n

        # File partagée entre les threads de réception et le thread principal
        self.message_queue = Queue()

        # Création de threads pour l'envoi et la réception
        self.recv_thread = threading.Thread(target=self.recv_thread_method, daemon=True)
        self.send_thread = threading.Thread(target=self.recv_thread_method, daemon=True)

    def running_state(self, state: bool): self.running = state

    def start(self):
        # Création de threads pour l'envoi et la réception
        self.recv_thread.start()
        self.send_thread.start()

    def stop(self):
        self.running = False
        time.sleep(1)
        self.recv_thread.join()
        self.send_thread.join()

    def recv_thread_method(self):  # Thread recv
        while self.running:
            try:
                data_recv = self.client.recv()

                data = pickle.loads(data_recv)  # pickle.loads() recompose l'object

                # Mettez les données dans la file pour que le thread principal les récupère
                self.message_queue.put(data)

            except socket.error as e:
                print("error")
                print(e)
                self.running = False

        print("Arret recv thread")

    def send_thread_method(self):  # Thread Send data
        pass

    def recv_treatment(self):
        pass


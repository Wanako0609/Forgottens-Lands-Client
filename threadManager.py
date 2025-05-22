import time
from queue import Queue
import pickle
import socket
import threading
import pygame
from network.network import Network
import treatment.treatment_recv as treatment
from screen.window import ScreenManager


class ThreadManager:

    def __init__(self, n: Network, screen: ScreenManager):

        self.running = True
        self.client = n

        # File partagée entre les threads de réception et le thread principal
        self.message_queue = Queue()

        # Création de threads pour l'envoi et la réception
        self.recv_thread = threading.Thread(target=self.recv_thread_method)
        self.send_thread = threading.Thread(target=self.send_actualisation_thread_method)

        # Creation thread de treatment
        self.recv_treatment_thread = threading.Thread(target=self.recv_treatment)

        self.screen = screen

    def running_state(self, state: bool): self.running = state

    def start(self):
        # Création de threads pour l'envoi et la réception
        self.recv_thread.start()
        self.send_thread.start()
        self.recv_treatment_thread.start()

    def stop(self):
        self.running = False

    def recv_thread_method(self):  # Thread recv
        while self.running:
            try:
                data_recv = self.client.recv()

                if not data_recv:
                    break

                data = pickle.loads(data_recv)  # pickle.loads() recompose l'object

                # Mettez les données dans la file pour que le thread principal les récupère
                self.message_queue.put(data)

            except socket.error as e:
                print("Error in recv thread methode")
                print(e)
                self.running = False

        print("Stop recv thread")

    def recv_treatment(self):
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(60)  # FPS

            try:
                # Récupérez les données de la file et utilisez-les dans la logique du jeu
                if not self.message_queue.empty():
                    data = self.message_queue.get()

                    treatment.treatment_data(data, self.screen)

            except socket.error as e:
                print("error in recv treatment")
                print(e)
                self.running = False

        print("Stop recv treatment thread")

    def send_actualisation_thread_method(self):  # Thread Send data
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)

            try:
                self.client.send(label="update_request", data="other_players")

            except socket.error as e:
                print("Error in recv thread methode")
                print(e)
                self.running = False


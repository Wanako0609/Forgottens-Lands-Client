import time

import pygame
import login.client_login as login
from network.network import Network
from screen.window import ScreenManager
from threadManager import ThreadManager

# Parametre
FPS = 60


def main():

    uuid = login.login_user()  # Envoie l'uuid du joueur courant

    print("Network connection start")
    # Connection serveur
    n = Network("127.0.0.1", 5555, uuid)

    print(n.get_player())
    print("Screen Manager Start")
    # Gestion Screen
    screen = ScreenManager(uuid)
    print("Screen")

    # Gestion des threads dans cette classe
    thread_manager = ThreadManager(n, screen)
    thread_manager.start()

    while thread_manager.running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                thread_manager.stop()
                n.close()
                screen.close()
                break

    print("Programme fini")


if __name__ == '__main__':
    main()

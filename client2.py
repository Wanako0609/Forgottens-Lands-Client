import pygame
import login.client_login as login
from network.network import Network
from network.threadManager import ThreadManager
from player import Player

# Parametre
FPS = 60

# Generation windows
width = 500
height = 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Forgotten Lands")


# Draw windows
def redrawWindow(player, players):
    #window.fill((255, 255,255 ))  # Clear to white

    # Dessine et centre le joueur actuel
    player.draw(window)
    # Gestion plusieurs joueurs
    for other_player in players:
        other_player.draw(window)

    pygame.display.flip()


def main():

    uuid = login.login_user()  # Envoie l'uuid du joueur courant

    # Connection serveur
    n = Network("127.0.0.1", 5555, uuid)

    # Gestion des threads dans cette classe
    thread_manager = ThreadManager(n)
    thread_manager.start()

    clock = pygame.time.Clock()

    while thread_manager.running:
        clock.tick(FPS)  # FPS

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                print("Programme fini")
                thread_manager.stop()
                pygame.quit()
                n.close()
                break


if __name__ == '__main__':
    main()

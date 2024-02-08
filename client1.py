import time

import pygame
import threading
import login.client_login as login
from network import Network
import player as p
from player import Player

# Parametre
FPS = 10

# Création d'un objet Event pour la synchronisation
update_event = threading.Event()

# Generation windows
width = 500
height = 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Forgotten Lands")

# Draw windows
def redrawWindow(window, player, players):
    window.fill((255, 255,255 ))  # Clear to white

    # Dessine et centre le joueur actuel
    #player.draw(window)
    # Gestion plusieurs joueurs
    for other_player in players:
        other_player.draw(window)

    pygame.display.update()


def send_data(n):

    # GESTION METHODES (ENVOI) #############################

    # Color
    space_pressed = False
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not space_pressed:
                space_pressed = True
                n.send(label="action", data="color")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

    # Move
    keys = p.move()
    n.send(label="player_move", data=keys)


def main():
    uuid = login.login_user()  # Envoie l'uuid du joueur courant

    # Connection serveur
    n = Network("127.0.0.1", 5555, uuid)

    # Recoit nos players data courantes
    player_data = n.get_player()
    player = Player(player_data)

    # Démarrez le thread network de réception
    n.start_threads()

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)  # FPS

        # Récupérez les données de la file et utilisez-les dans la logique du jeu
        if not n.message_queue.empty():
            data = n.message_queue.get()

            print(data)

        n.send(label="update_request", data="player_data")

        n.send(label="update_request", data="nb_players")

        n.send(label="update_request", data="other_players")

if __name__ == '__main__':
    main()
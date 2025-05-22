import pygame
import threading
import login.client_login as login
from network import Network
from entities import player as p
from entities.player import Player

# Parametre
FPS = 60


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


# Traite les données reçu
def getted_data(n, player):
    # Liste des players connecté
    players = []

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)  # FPS

        # Récupérez les données de la file et utilisez-les dans la logique du jeu
        if not n.message_queue.empty():
            data = n.message_queue.get()

            # GESTION ACTUALISATION JOUEUR #############################

            # # tuto Vérifiez l'étiquette pour déterminer le type de données
            # Actualise mes players data complete
            if data["label"] == "player_data":
                player_data = data["data"]
                # player.update_data()

            # Recoit le nombre de joueur connecté
            elif data["label"] == "nb_players":
                nb_players = data["data"]
                print(nb_players + " player connecté")
                nb_players = int(nb_players)  # Transtypage en int

            # Recoit joueurs connecté (class player client) pour le jeux
            elif data["label"] == "other_players":
                other_player_data = data["data"]
                other_player = Player(other_player_data)
                players.append(other_player)

            else:
                print("Mauvais format donnée")
                print(data)

            redrawWindow(window, player, players)
        else:
            n.send(label="update_request", data="nb_players")


def main():
    uuid = login.login_user()  # Envoie l'uuid du joueur courant

    # Connection serveur
    n = Network("127.0.0.1", 5555, uuid)

    # Recoit nos players data courantes
    player_data = n.get_player()
    player = Player(player_data)

    # Démarrez le thread network de réception
    n.start_threads()


    # Crée les threads de traitement et d'envoie
    recv = threading.Thread(target=getted_data, args=(n, player))
    send = threading.Thread(target=send_data, args=(n,))

    # Démarrer les threads
    recv.start()
    send.start()

    # Boucle jeu
    run = True
    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break

    recv.join()
    send.join()
    n.close()
    pygame.quit()


if __name__ == '__main__':
    main()
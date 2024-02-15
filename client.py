import pygame
import login.client_login as login
from network import Network
from player import Player

# Parametre
FPS = 60


# Generation windows
width = 500
height = 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Forgotten Lands")

# Go to upd

# Draw windows
def redrawWindow(window, player, players):
    window.fill((255,255,255))  # Clear to white

    # Dessine et centre le joueur actuel
    #player.draw(window)
    # Gestion plusieurs joueurs
    for other_player in players:
        other_player.draw(window)

    print("e")
    pygame.display.update()


def main():
    uuid = login.login_user()  # Envoie l'uuid du joueur courant

    # Connection serveur
    n = Network("127.0.0.1", 5555, uuid)

    # Recoit nos players data courantes
    player_data = n.get_player()
    #print(player_data)
    player = Player(player_data)

    # Liste des players connecté
    players = []

    # Boucle jeu
    run = True
    clock = pygame.time.Clock()
    print("boucle du jeux")
    while run:
        clock.tick(FPS)  # FPS
        print("loop")
        try:
            # GESTION ACTUALISATION JOUEUR #############################

            # Actualise mes players data complete
            player_data = n.rcv_obj()
            #print("players data")
            #print(player_data)
            #player.update_data()

            # Recoit le nombre de joueur connecté
            nb_players = n.rcv_str()
            #print(nb_players + " player connecté")
            print("a")


            # Recoit la liste des joueurs connecté avec leurs informations imperative (class player client) pour le jeux
            nb_players = int(nb_players)  # Transtypage en int
            players = []  # Clear la liste

            for i in range(nb_players):
                other_current_playerdata = n.rcv_obj()
                other_current_player = Player(other_current_playerdata)
                players.append(other_current_player)

            print("b")
            # GESTION METHODES #############################

            # Gestion des methodes coté client (Move, color_set)

            keys_action = [0]
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False
                    # Envoyé la deconnection
                    n.close()
                    pygame.quit()
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        keys_action[0] = [1]

            # Move
            keys = player.move()
            n.send_obj(keys)
            print("c")

            # Color
            n.send_obj(keys_action)
            print("d")
            # Avec la liste des joueurs connecté
            redrawWindow(window, player, players)
            print("f")

            del players
            #del keys
            #del keys_action
            del other_current_player
            del other_current_playerdata
            del nb_players
        except Exception as e:
            print(e)
            print("Reconnexion en cours")
            n = Network("127.0.0.1", 5555, uuid)
            continue


if __name__ == '__main__':
    main()
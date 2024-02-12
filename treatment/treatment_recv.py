# Fonction de tratement de donnée
from player import Player


def other_player_gestion():
    pass

# Traite les données reçu
def treatment_data(n, player):

    # Liste des players connecté
    #players = []
    players = [Player({"x": 10, "y": 10, "color": (0, 255, 0)}), Player({"x": 100, "y": 100, "color": (0, 0, 255)})]

    clock = pygame.time.Clock()

    while run:
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

            elif data["label"] == "other_players_start":
                players = []

            # Recoit joueurs connecté (class player client) pour le jeux
            elif data["label"] == "other_players":
                other_player_data = data["data"]
                other_player_data = data["data"]
                other_player = Player(other_player_data)
                players.append(other_player)

            else:
                print("Mauvais format donnée")
                print(data)

        # else:
        # n.send(label="update_request", data="other_players")

        if run:
            redrawWindow(player, players)

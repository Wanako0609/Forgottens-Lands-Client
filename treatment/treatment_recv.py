# Fonction de tratement de donnée
from entities.player import Player
from screen.window import ScreenManager


def treatment_data(data, screen: ScreenManager):

    # GESTION ACTUALISATION JOUEUR #############################

    # # tuto Vérifiez l'étiquette pour déterminer le type de données
    # Actualise mes players data complete
    if data["label"] == "player_data":
        player_data = data["data"]
        # player.update_data()

    elif data["label"] == "other_players_start":
        screen.connect_players_clear()

    # Recoit joueurs connecté (class player client) pour le jeux
    elif data["label"] == "other_players":
        other_player_data = data["data"]
        other_player = Player(other_player_data)
        screen.connect_players_append(other_player)

    elif data["label"] == "other_players_end":
        screen.connect_players_full()
        print("t")

    else:
        print("Mauvais format donnée")
        print(data)

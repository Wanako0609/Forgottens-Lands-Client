import pygame
from entities.player import Player


class ScreenManager:
    def __init__(self, uuid):

        # Generation windows
        self.width = 500
        self.height = 500
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Forgotten Lands")

        # Liste des players connecté
        self.connect_players = []
        #players = [Player({"x": 10, "y": 10, "color": (0, 255, 0)}), Player({"x": 100, "y": 100, "color": (0, 0, 255)})]

        self.uuid = uuid

    def connect_players_append(self, player): self.connect_players.append(player)

    def connect_players_clear(self): self.connect_players = []

    def connect_players_full(self): self.updateWindow()

    def updateWindow(self):
        # window.fill((255, 255,255 ))  # Clear to white

        # Dessine et centre le joueur actuel
        #self.current_player.draw(self.window)
        print("e")
        # Gestion plusieurs joueurs
        for other_player in self.connect_players:
            other_player.draw(self.window)

        pygame.display.flip()

    def close(self): pygame.quit()

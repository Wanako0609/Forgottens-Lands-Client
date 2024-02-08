import pygame


# Crée une class entité et currentPlayer
class Player:

    def __init__(self, playerdata):
        self.x = playerdata["x"]
        self.y = playerdata["y"]
        self.width = 100
        self.height = 100
        self.color = playerdata["color"]
        self.rect = (self.x, self.y, self.width, self.height)
        self.speed = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update_data(self, player_data):
        pass

    def update_rect(self):
        self.rect = (self.x, self.y, self.width, self.height)


def move():
    pressed = pygame.key.get_pressed()
    keys = []

    if pressed[pygame.K_q]:
        # self.x -= self.speed
        keys.append("left")

    if pressed[pygame.K_d]:
        # self.x += self.speed
        keys.append("right")

    if pressed[pygame.K_z]:
        # self.y -= self.speed
        keys.append("up")

    if pressed[pygame.K_s]:
        # self.y += self.speed
        keys.append("down")

    return keys

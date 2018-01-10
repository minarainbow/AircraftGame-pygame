import random
import pygame

pad_width = 1200
pad_height = 600

class Aircraft:
    def __init__(self):
        self.x = pad_width * 0.05
        self.y = pad_height * 0.4
        self.height = 55
        self.width = 89
        self.image = pygame.image.load('images/plane.png')

    def draw(self, gamepad):
        gamepad.blit(self.image, (self.x, self.y))


class Fire:
    def __init__(self, filename, width, height):
        self.x = pad_width
        self.y = random.randrange(0, pad_height - height)
        self.height = height
        self.width = width
        self.image = pygame.image.load('images/' + filename)

    def draw(self, gamepad):
        gamepad.blit(self.image, (self.x, self.y))

class Bat:
    def __init__(self):
        self.x = pad_width
        self.y = random.randrange(0, pad_height - 70)
        self.height = 139
        self.width = 70
        self.image = pygame.image.load('images/bat.png')
        self.isShot = False

    def move(self, speed):
        self.x -= speed
        if self.x <= 0:
            self.x = pad_width
            self.y = random.randrange(0, pad_height - 70)

    def draw(self, gamepad):
        gamepad.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.height = 5
        self.width = 27
        self.image = pygame.image.load('images/bullet.png')

    def draw(self, gamepad):
        gamepad.blit(self.image, (self.x, self.y))

import pygame
import random
from time import sleep

import objects
import title

from optparse import OptionParser

PAD_WIDTH = 1200
PAD_HEIGHT = 600

def option_parser():
    parser = OptionParser()
    parser.add_option("-d", "--hardcore", dest="hardcore", action="store_true", help="hardcore mode on", default=False)

    return parser.parse_args()


def initGame():
    global gamepad, clock, background1, background2
    global boom, shot_sound, explosion_sound
    global options, args
    (options, args) = option_parser()

    pygame.init()

    shot_sound = pygame.mixer.Sound('sounds/shot.wav')
    explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')

    gamepad = pygame.display.set_mode((PAD_WIDTH, PAD_HEIGHT))
    pygame.display.set_caption("PyFlight")

    gameTitle = title.GameTitle(gamepad)
    gameTitle.show()

initGame()

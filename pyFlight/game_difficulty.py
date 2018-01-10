import pygame

import game
from objects import *
from time import sleep

BLACK = (0, 0, 0)
RED = (255, 0, 0)

class GameDifficulty:
    def __init__(self, gamepad):
        self.gamepad = gamepad
        self.PAD_WIDTH, self.PAD_HEIGHT = gamepad.get_size()
        self.font = pygame.font.SysFont('purisa', 60)

        self.BACKGROUND_SPEED = 2

    def show(self):
        clock = pygame.time.Clock()

        self.gamepad.fill((255, 255, 255))
        background1 = pygame.image.load('images/background.png')
        background2 = background1.copy()
        background_width = background1.get_width()
        background1_x = 0
        background2_x = background_width

        easyBtn = pygame.Surface((420, 100))
        easyBtn.fill((60, 60, 60))
        easyBtn.set_alpha(100)
        normalBtn = easyBtn.copy()
        nightmareBtn = easyBtn.copy()

        easyText = self.font.render("EASY", True, BLACK)
        easyRect = easyText.get_rect()
        easyRect.center = (self.PAD_WIDTH/2, self.PAD_HEIGHT*0.2)
        easyBtnRect = easyBtn.get_rect()
        easyBtnRect.center = (self.PAD_WIDTH/2, self.PAD_HEIGHT*0.2)

        normalText = self.font.render("NORMAL", True, BLACK)
        normalRect = normalText.get_rect()
        normalRect.center = (self.PAD_WIDTH/2, self.PAD_HEIGHT*0.5)
        normalBtnRect = normalBtn.get_rect()
        normalBtnRect.center = (self.PAD_WIDTH/2, self.PAD_HEIGHT*0.5)

        nightmareText = self.font.render("NIGHTMARE", True, RED)
        nightmareRect = nightmareText.get_rect()
        nightmareRect.center = (self.PAD_WIDTH/2, self.PAD_HEIGHT*0.8)
        nightmareBtnRect = nightmareBtn.get_rect()
        nightmareBtnRect.center = (self.PAD_WIDTH/2, self.PAD_HEIGHT*0.8)

        isOver = False
        while not isOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isOver = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if easyRect.collidepoint(mouse_pos):
                        gameEasy = game.Game(self.gamepad, "Easy")
                        gameEasy.run()
                    elif normalRect.collidepoint(mouse_pos):
                        gameNormal = game.Game(self.gamepad, "Normal")
                        gameNormal.run()
                    elif nightmareRect.collidepoint(mouse_pos):
                        gameNightmare = game.Game(self.gamepad, "Nightmare")
                        gameNightmare.run()

            background1_x -= self.BACKGROUND_SPEED
            background2_x -= self.BACKGROUND_SPEED

            if background1_x == -background_width:
                background1_x = background_width

            if background2_x == -background_width:
                background2_x = background_width

            self.gamepad.blit(background1, (background1_x, 0))
            self.gamepad.blit(background2, (background2_x, 0))

            self.gamepad.blit(easyBtn, easyBtnRect)
            self.gamepad.blit(normalBtn, normalBtnRect)
            self.gamepad.blit(nightmareBtn, nightmareBtnRect)

            self.gamepad.blit(easyText, easyRect)
            self.gamepad.blit(normalText, normalRect)
            self.gamepad.blit(nightmareText, nightmareRect)

            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        quit()

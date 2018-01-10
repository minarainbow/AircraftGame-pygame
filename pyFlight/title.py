import pygame
from time import sleep

from objects import *
import game_difficulty
import rank_difficulty

class GameTitle:
    def __init__(self, gamepad):
        self.gamepad = gamepad
        self.PAD_WIDTH, self.PAD_HEIGHT = gamepad.get_size()

        self.BACKGROUND_SPEED = 2

    def show(self):
        clock = pygame.time.Clock()

        button_width = 150
        button_height = 70
        startBtn = pygame.Surface((button_width, button_height))
        startBtn.fill((60, 60, 60))
        startBtn.set_alpha(100)
        rankBtn = startBtn.copy()
        quitBtn = startBtn.copy()

        pygame.font.init()
        titleFont = pygame.font.SysFont('purisa', 80)
        menuFont = pygame.font.SysFont('purisa', 30)

        gameTitle = titleFont.render('PI-YONG', True, (0, 0, 0))
        titleRect = gameTitle.get_rect()
        titleRect.center = (self.PAD_WIDTH/2, self.PAD_HEIGHT*0.3)

        startText = menuFont.render('Start', True, (0, 0, 0))
        startRect = startText.get_rect()
        startRect.center = (self.PAD_WIDTH*0.3, self.PAD_HEIGHT*0.6)
        startBtnRect = startBtn.get_rect()
        startBtnRect.center = (self.PAD_WIDTH*0.3, self.PAD_HEIGHT*0.6)

        rankText = menuFont.render('Rank', True, (0, 0, 0))
        rankRect = rankText.get_rect()
        rankRect.center = (self.PAD_WIDTH*0.5, self.PAD_HEIGHT*0.6)
        rankBtnRect = rankBtn.get_rect()
        rankBtnRect.center = (self.PAD_WIDTH*0.5, self.PAD_HEIGHT*0.6)

        quitText = menuFont.render('Quit', True, (0, 0, 0))
        quitRect = quitText.get_rect()
        quitRect.center = (self.PAD_WIDTH*0.7, self.PAD_HEIGHT*0.6)
        quitBtnRect = quitBtn.get_rect()
        quitBtnRect.center = (self.PAD_WIDTH*0.7, self.PAD_HEIGHT*0.6)

        background1 = pygame.image.load('images/background.png')
        background2 = background1.copy()
        background_width = background1.get_width()
        background1_x = 0
        background2_x = background_width

        isOver = False
        while not isOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isOver = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if startRect.collidepoint(mouse_pos):
                        gameDifficulty = game_difficulty.GameDifficulty(self.gamepad)
                        gameDifficulty.show()
                    elif rankRect.collidepoint(mouse_pos):
                        rankDifficulty = rank_difficulty.RankDifficulty(self.gamepad)
                        rankDifficulty.show()
                    elif quitRect.collidepoint(mouse_pos):
                        isOver = True

            background1_x -= self.BACKGROUND_SPEED
            background2_x -= self.BACKGROUND_SPEED

            if background1_x == -background_width:
                background1_x = background_width

            if background2_x == -background_width:
                background2_x = background_width


            self.gamepad.fill((255, 255, 255))
            self.gamepad.blit(background1, (background1_x, 0))
            self.gamepad.blit(background2, (background2_x, 0))
            self.gamepad.blit(gameTitle, titleRect)

            self.gamepad.blit(startText, startRect)
            self.gamepad.blit(startBtn, startBtnRect)

            self.gamepad.blit(rankText, rankRect)
            self.gamepad.blit(rankBtn, rankBtnRect)

            self.gamepad.blit(quitText, quitRect)
            self.gamepad.blit(quitBtn, quitBtnRect)

            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        quit()

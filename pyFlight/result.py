import random
import pygame
import requests
import json

import title

MESSAGE = "Press 'Enter' to return menu or 'Q' to quit game"
URL = "http://52.79.185.2:8080/api/scores"

class GameResult:
    def __init__(self, gamepad, nickname, score, difficulty):
        self.gamepad = gamepad
        self.PAD_WIDTH, self.PAD_HEIGHT = gamepad.get_size()

        self.nickname = nickname
        self.score = score
        self.difficulty = difficulty

        self.BACKGROUND_SPEED = 2

    def show(self):
        clock = pygame.time.Clock()

        self.gamepad.fill((255, 255, 255))
        background1 = pygame.image.load('images/background.png')
        background2 = background1.copy()
        background_width = background1.get_width()
        background1_x = 0
        background2_x = background_width
        message_count = 0
        ranking_list = self._send_result()
        self._fade_in()

        isOver = False
        while not isOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isOver = True

                if event.type == pygame.KEYDOWN:
                    inkey = event.key
                    if inkey in [13, 271]:
                        gameTitle = title.GameTitle(self.gamepad)
                        gameTitle.show()
                    elif inkey == pygame.K_q:
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
            self._show_score_board(ranking_list)

            msgFont = pygame.font.Font("freesansbold.ttf", 30)
            msgSurf = msgFont.render(MESSAGE, True, (0, 0, 0))
            msgRect = msgSurf.get_rect()
            msgRect.center = ((self.PAD_WIDTH/2, 570))

            if message_count < 60:
                message_count += 1
                self.gamepad.blit(msgSurf, msgRect)
            else:
                message_count += 1
                if message_count == 120:
                    message_count = 0

            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        quit()

    def _fade_in(self):
        clock = pygame.time.Clock()

        background1 = pygame.image.load('images/background.png')
        background2 = background1.copy()
        background_width = background1.get_width()
        background1_x = 0
        background2_x = background_width
        ranking_list = []

        alpha = 255
        fade_in_effect = pygame.Surface((self.PAD_WIDTH, self.PAD_HEIGHT))
        fade_in_effect.fill((0, 0, 0))

        while alpha > 0:
            alpha -= 4

            self.gamepad.blit(background1, (background1_x, 0))
            self.gamepad.blit(background2, (background2_x, 0))

            self._show_score_board(ranking_list)

            fade_in_effect.set_alpha(alpha)
            self.gamepad.blit(fade_in_effect, (0, 0))

            pygame.display.update()
            clock.tick(60)

    def _send_result(self):
        data = {'nickname': self.nickname, 'score': self.score, 'mode': self.difficulty}
        result = None
        try:
            if self.nickname == 'RRRR':
                res = requests.post(URL+"3", data = data)
                result = res.json()
            else:
                res = requests.post(URL, data = data)
                result = res.json()
        except:
            result = [{'nickname': 'RAN', 'score': 250, 'mode': 'Nightmare'}]

        return result

    def _show_score_board(self, results):
        ranking_list = []

        for result in results:
            ranking_list.append([result['nickname'], result['score']])
        while (len(ranking_list) < 10):
            ranking_list.append(["___", "___"])

        scoreBoard = pygame.Surface((900, 480))
        scoreBoard.fill((60, 60, 60))
        scoreBoard.set_alpha(200)

        pygame.font.init()
        titleFont = pygame.font.SysFont('purisa', 40)
        rankFont = pygame.font.SysFont('purisa', 40)

        resultTitle = titleFont.render('High Score (' +self.difficulty+ ')', True, (255, 255, 255))
        resultRect = resultTitle.get_rect()
        resultRect.center = ((self.PAD_WIDTH/2), 100)

        self.gamepad.blit(scoreBoard, (150, 60))
        self.gamepad.blit(resultTitle, resultRect)
        for i, ranker in enumerate(ranking_list):
            nickname = ranker[0]
            score = ranker[1]
            if len(nickname) == 0:
                nickname = "    "
            elif len(nickname) == 1:
                nickname = " " + nickname + " "
            elif len(nickname) == 2:
                nickname = nickname + " "

            rank = str(i+1) + "." + "  " + nickname + "  " + str(score)
            rankSurf = rankFont.render(rank, True, (255, 255, 255))
            rankRect = rankSurf.get_rect()
            if i < 5:
                rankRect.center = ((350, 160 + i * 80))
            else:
                rankRect.center = ((850, 160 + (i-5) * 80))
            self.gamepad.blit(rankSurf, rankRect)

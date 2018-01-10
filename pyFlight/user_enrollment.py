import random
import pygame
import requests
import json

from result import GameResult

MESSAGE = "Enter Your Name"
URL = "http://52.79.185.2:8080/api/scores"

GREY = (200,200,200)
WHITE=(255,255,255)
BLACK=(0,0,0)

class UserEnrollment:
    def __init__(self, gamepad, score, difficulty):
        self.gamepad = gamepad
        self.PAD_WIDTH, self.PAD_HEIGHT = gamepad.get_size()

        self.BACKGROUND_SPEED = 2
        self.score = score
        self.difficulty = difficulty

    def show(self):
        """ 보여주는 함수"""
        clock = pygame.time.Clock()

        # 화면 초기화
        self.gamepad.fill((255, 255, 255))

        # 배경 설정값
        background1 = pygame.image.load('images/background.png')
        background2 = background1.copy()
        background_width = background1.get_width()
        background1_x = 0
        background2_x = background_width
        name = ""

        self._fade_in()

        isOver = False
        while not isOver:
            # 이벤트 핸들러
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isOver = True

                if event.type == pygame.KEYDOWN:
                    inkey = event.key
                    if inkey in [13, 271]:  # enter/return key
                        game_result = GameResult(self.gamepad, name, self.score, self.difficulty)
                        game_result.show()
                    elif inkey == 8:
                        name = name[:-1]
                    elif inkey <= 300:
                        if ((pygame.key.get_mods() & pygame.KMOD_SHIFT)
                            and (122 >= inkey >= 97)):
                            inkey -= 32
                        if len(name) == 3:
                            name = name[:-1]
                        name += chr(inkey)

            # 배경 움직이기 시작
            background1_x -= self.BACKGROUND_SPEED
            background2_x -= self.BACKGROUND_SPEED

            if background1_x == -background_width:
                background1_x = background_width

            if background2_x == -background_width:
                background2_x = background_width

            self.gamepad.fill((255, 255, 255))
            self.gamepad.blit(background1, (background1_x, 0))
            self.gamepad.blit(background2, (background2_x, 0))
            # 배경 움직이기 끝

            name = name.upper()
            self._show_input_window(name)

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
        name = ""

        alpha = 255
        fade_in_effect = pygame.Surface((self.PAD_WIDTH, self.PAD_HEIGHT))
        fade_in_effect.fill((0, 0, 0))

        while alpha > 0:
            alpha -= 4

            self.gamepad.blit(background1, (background1_x, 0))
            self.gamepad.blit(background2, (background2_x, 0))

            self._show_input_window(name)

            fade_in_effect.set_alpha(alpha)
            self.gamepad.blit(fade_in_effect, (0, 0))

            pygame.display.update()
            clock.tick(60)

    def _show_input_window(self, name):
        """닉네임 인풋 창 띄우기 // 글자수 3개로 제한 """
        scoreBoard = pygame.Surface((900, 480))
        scoreBoard.fill((60, 60, 60))
        scoreBoard.set_alpha(200)
        self.gamepad.blit(scoreBoard, (150, 60))

        wrapped_box_width = 600
        wrapped_box_height = 250
        text_box_width = wrapped_box_width * 0.8
        text_box_height = wrapped_box_height * 0.4

        wrapped_box = pygame.Surface((wrapped_box_width, wrapped_box_height))
        wrapped_box.fill(GREY)
        wrapBoxRect = wrapped_box.get_rect()
        wrapBoxRect.center = (self.PAD_WIDTH/2, self.PAD_HEIGHT/2)

        text_box = pygame.Surface((text_box_width, text_box_height))
        text_box.fill(WHITE)
        textBoxRect = text_box.get_rect()
        textBoxRect.center = (wrapped_box_width/2, wrapped_box_height*0.55)

        font = pygame.font.SysFont("purisa", 40)
        msgText = font.render(MESSAGE, True, BLACK)
        msgRect = msgText.get_rect()
        msgRect.center = (wrapped_box_width/2, wrapped_box_height*0.2)

        okFont = pygame.font.SysFont("purisa", 30)
        okText = okFont.render("OK", True, BLACK)
        okRect = okText.get_rect()
        okRect.center = (wrapped_box_width/2, wrapped_box_height*0.9)

        input_name = font.render(name, True, BLACK)
        input_name_rect = input_name.get_rect()
        input_name_rect.center = (text_box_width/2, text_box_height/2)

        text_box.blit(input_name, input_name_rect)
        wrapped_box.blit(text_box,textBoxRect)
        wrapped_box.blit(msgText, msgRect)
        wrapped_box.blit(okText, okRect)
        self.gamepad.blit(wrapped_box, wrapBoxRect)

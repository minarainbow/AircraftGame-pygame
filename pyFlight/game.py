import pygame
import requests

from objects import *
from time import sleep
import user_enrollment
import result

NOT_IN_RANK = 0
LOWEST_IN_RANK = 1
IN_RANK = 2

URL = "http://52.79.185.2:8080/api/scores2"

class Game:
    def __init__(self, gamepad, difficulty):
        self.gamepad = gamepad
        self.PAD_WIDTH, self.PAD_HEIGHT = gamepad.get_size()

        self.score = 0
        self.difficulty = difficulty
        self.num_fire = 1
        self.bullets = []
        self.bats = []
        self.fires = []
        self.firesInfo = [1, 2, 0, 0, 0]

        self.AIRCRAFT_SPEED = 12
        self.BAT_SPEED = 4
        self.FIRE_SPEED = 6
        self.BULLET_SPEED = 12
        self.BACKGROUND_SPEED = 2

        self.fire1_width = 140
        self.fire1_height = 61
        self.fire2_width = 86
        self.fire2_height = 59

    def run(self):
        """ Start Game """
        clock = pygame.time.Clock()

        # Set Objects
        aircraft = Aircraft()
        y_change = 0

        boom = pygame.image.load('images/boom.png')
        boom_count = 0

        background1 = pygame.image.load('images/background.png')
        background2 = background1.copy()
        background_width = background1.get_width()
        background1_x = 0
        background2_x = background_width

        self.bats.append(Bat())
        fire_x = self.PAD_WIDTH

        # Main Loop
        gameOver = False
        isChange = False
        while not gameOver:
            # Game Difference Handler
            if self.score % 10 == 1:
                isChange = False

            if self.difficulty == "Nightmare":
                if not isChange:
                    isChange = self.level_up()
            else:
                if not isChange and self.score <= 100:
                    isChange = self.level_up()

            # Event Handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        y_change = -self.AIRCRAFT_SPEED
                    elif event.key == pygame.K_DOWN:
                        y_change = self.AIRCRAFT_SPEED
                    elif event.key == pygame.K_LCTRL:
                        #pygame.mixer.Sound.play(shot_sound)
                        bullet_x = aircraft.x + aircraft.width
                        bullet_y = aircraft.y + aircraft.height / 2
                        self.bullets.append(Bullet(bullet_x, bullet_y))
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        y_change = 0

            # Aircraft Movement
            aircraft.y += y_change
            if aircraft.y < 0:
                aircraft.y = 0
            elif aircraft.y + aircraft.height > self.PAD_HEIGHT:
                aircraft.y = self.PAD_HEIGHT - aircraft.height

            # Background Movement
            background1_x -= self.BACKGROUND_SPEED
            background2_x -= self.BACKGROUND_SPEED
            if background1_x == -background_width:
                background1_x = background_width
            if background2_x == -background_width:
                background2_x = background_width

            # Make self.fires according to FireInfo List
            while len(self.fires) != self.num_fire:
                index = random.randrange(0, len(self.firesInfo))
                if self.firesInfo[index] == 0:
                    self.fires.append(None)
                elif self.firesInfo[index] == 1:
                    self.fires.append(Fire('fireball.png', self.fire1_width, self.fire1_height))
                elif self.firesInfo[index] == 2:
                    self.fires.append(Fire('fireball2.png', self.fire2_width, self.fire2_height))

            # Fire Movement
            for fire in self.fires:
                if fire == None:
                    fire_x -= (0.5 * self.FIRE_SPEED)
                    if fire_x <= 0:
                        self.fires.remove(fire)
                        fire_x = self.PAD_WIDTH
                else:
                    fire.x -= self.FIRE_SPEED
                    if fire.x <= 0:
                        self.fires.remove(fire)
                        self.score += 1

            # Bat Movement
            for bat in self.bats:
                bat.move(self.BAT_SPEED)

            # Bullet Movement
            if len(self.bullets) != 0:
                for bullet in self.bullets:
                    bullet.x += self.BULLET_SPEED
                    if bullet.x >= self.PAD_WIDTH:
                        self.bullets.remove(bullet)
                        continue
                    for bat in self.bats:
                        if bullet.x >= bat.x:
                            if bullet.y > bat.y and bullet.y < bat.y + bat.height:
                                self.bullets.remove(bullet)
                                #self.score += 1
                                bat.isShot = True
                                break

            # Game Over Statement
            for bat in self.bats:
                if ((aircraft.x + aircraft.width > bat.x + 30)
                    and (aircraft.x + 30 < bat.x + bat.width)
                    and (not bat.isShot)):
                    if ((aircraft.y + 30 < bat.y + bat.height)
                        and (aircraft.y + aircraft.height > bat.y + 30)):
                        self.crash()

            if fire != None:
                if ((aircraft.x + aircraft.width > fire.x + 30)
                    and (aircraft.x + 30 < fire.x + fire.height)):
                    if ((aircraft.y + 30 < fire.y + fire.height)
                        and (aircraft.y + aircraft.height > fire.y + 30)):
                        self.crash()

            for fire in self.fires:
                if fire == None:
                    continue
                if aircraft.x + aircraft.width / 2 > fire.x:
                    if ((aircraft.y < fire.y + fire.height / 2)
                        and (aircraft.y > fire.y - fire.height / 2)):
                        self.crash()

            # Re - Draw
            self.gamepad.fill((255, 255, 255))
            self.gamepad.blit(background1, (background1_x, 0))
            self.gamepad.blit(background2, (background2_x, 0))

            for bat in self.bats:
                if bat.isShot:
                    self.gamepad.blit(boom, (bat.x, bat.y))
                    self.score += 1
                    boom_count += 1
                    if boom_count == 5:
                        boom_count = 0
                        bat.x = self.PAD_WIDTH
                        bat.y = random.randrange(0, self.PAD_HEIGHT - bat.height)
                        bat.isShot = False
                else:
                    bat.draw(self.gamepad)

            aircraft.draw(self.gamepad)
            for fire in self.fires:
                if fire == None:
                    continue
                fire.draw(self.gamepad)

            for bullet in self.bullets:
                bullet.draw(self.gamepad)

            scoreFont = pygame.font.Font('freesansbold.ttf', 30)
            scoreText = scoreFont.render("score: " + str(self.score), True, (0,0,0))
            self.gamepad.blit(scoreText, (self.PAD_WIDTH/2, 0))
            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        quit()

    def crash(self):
        """ When aircraft crashed with objects, diplay message "CRASH"
            and go to result screen """
        #pygame.mixer.Sound.play(explosion_sound)
        largeText = pygame.font.Font('freesansbold.ttf', 200)
        textSurf = largeText.render('Crashed', True, (255, 0, 0))
        textRect = textSurf.get_rect()

        textRect.center = ((self.PAD_WIDTH/2), (self.PAD_HEIGHT/2))
        self.gamepad.blit(textSurf, textRect)
        self._fade_out()

        is_ranker = self._is_in_rank()
        if is_ranker == IN_RANK:
            userEnrollment = user_enrollment.UserEnrollment(self.gamepad, self.score, self.difficulty)
            userEnrollment.show()
        elif is_ranker == LOWEST_IN_RANK:
            userEnrollment = user_enrollment.UserEnrollment(self.gamepad, self.score, self.difficulty)
            userEnrollment.show()
        elif is_ranker == NOT_IN_RANK:
            print("not int ranker TT")
            game_result = result.GameResult(self.gamepad, 'RRRR', self.score, self.difficulty)
            game_result.show()

    def _fade_out(self):
        clock = pygame.time.Clock()

        shut_down_effect = pygame.Surface((self.PAD_WIDTH, self.PAD_HEIGHT))
        shut_down_effect.fill((0, 0, 0))
        alpha = 0

        while alpha < 13:
            alpha += 0.1
            shut_down_effect.set_alpha(alpha)
            self.gamepad.blit(shut_down_effect, (0, 0))

            pygame.display.update()
            clock.tick(60)

    def _is_in_rank(self):
        try:
            data = {'mode': self.difficulty}
            res = requests.post(URL, data = data)
            results = res.json()
            if len(results) == 0:
                return IN_RANK
            for result in results:
                rank_score = result['score']
                if self.score > rank_score:
                    return IN_RANK
                elif self.score == rank_score:
                    return LOWEST_IN_RANK
                else:
                    return NOT_IN_RANK
        except:
            print("EXCEPTION")
            return IN_RANK

    def level_up(self):
        """ Speed up objects and increase number of objects """
        result = False

        if self.score % 10 == 0:
            self.BAT_SPEED += 0.5
            self.FIRE_SPEED += 0.5
            result = True

        if self.score % 20 == 0 and self.score != 0:
            new_bat = Bat()
            self.bats.append(new_bat)
            self.firesInfo += [0, 1, 2]
            self.num_fire += 1

        return result

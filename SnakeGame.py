import pygame
import random
from pygame.locals import *
import time

SIZE = 40


class Snake:
    def __init__(self, surface, length):
        self.parent_screen = surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.direction = "down"

        self.length = length
        self.x = [40] * length
        self.y = [40] * length

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        self.draw()

    def draw(self):
        self.parent_screen.fill((110, 110, 5))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Apple():
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple-removebg-preview.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 25) * SIZE
        self.y = random.randint(1, 20) * SIZE


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake game")
        pygame.mixer.init()
        self.play_backround_music()
        self.surface = pygame.display.set_mode((1500, 950))
        self.snake = Snake(self.surface, 5)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_backround_music(self):
        pygame.mixer.music.load("resources/Backroundmusic.mp3")
        pygame.mixer.music.play(-1,0)

    def play_sound(self,sound_name):
        if sound_name == "crash":
            sound=pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name=="ding":
            sound=pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False


    def play(self):

        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Collision occured"
        if not (0<=self.snake.x[0] <= 1500 and 0 <= self.snake.y[0] <= 950):
            self.play_sound("crash")
            raise "Hit the boundary error"

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f'Score:{self.snake.length - 1}', True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def show_game_over(self):
        self.surface.fill((50,50,50))
        font = pygame.font.SysFont("arial",30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1,(200,300))
        line2 = font.render("To play again press Enter. To exit press Escape",True,(255,255,255))
        self.surface.blit(line2,(200,500))
        pygame.mixer.music.pause()


        pygame.display.flip()
    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running=False
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)


if __name__ == "__main__":
    game = Game()
    game.run()


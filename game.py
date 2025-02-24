import pygame
import level as l
import game_info as gi
import collision as cl
import car
from utils import blit_text_center

class Game:
    def __init__(self, fps=60):
        pygame.font.init()
        self.level = l.Level()
        self.width, self.height = self.level.width, self.level.height
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Racing Game!")
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True
        self.font = pygame.font.SysFont("comicsans", 44)
        self.game_info = gi.GameInfo()
        self.car = car.Car(4, 4)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_events()

            if not self.game_info.started:
                self.draw()
                blit_text_center(self.win, self.font, "Press any key to start!")
                pygame.display.update()
                continue

            self.car.move()
            cl.Collision.handle_collision(self.car, self.game_info, self.level, self.win, self.font)  # Передаємо рівень

            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and not self.game_info.started:
                self.game_info.start_game()

        if self.game_info.started:
            keys = pygame.key.get_pressed()
            self.car.handle_movement(keys)

    def draw(self):
        self.level.draw(self.win)
        time_text = self.font.render(f"Time: {self.game_info.get_time()}s", 1, (255, 255, 255))
        self.win.blit(time_text, (10, self.height - 40))
        self.car.draw(self.win)
        pygame.display.update()
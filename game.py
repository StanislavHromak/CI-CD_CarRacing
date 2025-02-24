import pygame
import level as l
import game_info as gi
import collision as cl
import car
import menu as mn
from utils import blit_text_center

class Game:
    def __init__(self, fps=60):
        self.car = None
        self.game_info = None
        self.level = None
        pygame.font.init()
        self.running = True
        self.fps = fps
        self.level_number = 1

        # Меню
        self.width, self.height = 800, 600
        self.win = pygame.display.set_mode((self.width, self.height))
        self.menu = mn.Menu(self.win, self.width, self.height)

    def run(self):
        while self.running:
            selected_option = self.show_menu()
            if selected_option == 0:  # Почати гру
                self.play_levels()
            elif selected_option == 3:  # Вихід
                self.running = False

        pygame.quit()

    def show_menu(self):
        while self.running:
            self.menu.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
            selected = self.menu.handle_input()
            if selected is not None:
                return selected

    def play_levels(self):
        while self.level_number <= 5:
            result = self.play_level()
            if result == "menu":  # Якщо гравець програв, повертаємось у меню
                break
            self.level_number += 1
        self.level_number = 1  # Після завершення повертаємося в меню

    def play_level(self):
        self.level = l.Level()
        self.game_info = gi.GameInfo()
        self.car = car.Car(4, 4)
        self.win = pygame.display.set_mode((self.level.width, self.level.height))
        pygame.display.set_caption(f"Racing Game! Level {self.level_number}")
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(self.fps)
            self.handle_events()

            if not self.game_info.started:
                self.draw()
                blit_text_center(self.win, pygame.font.SysFont("comicsans", 44), "Press any key to start!")
                pygame.display.update()
                continue

            self.car.move()
            result = cl.Collision.handle_collision(self.car, self.game_info, self.level, self.win,
                                                pygame.font.SysFont("comicsans", 44))

            self.draw()

            # Якщо гра завершена (перемога або поразка)
            if result == "menu":  # Програш → вихід у меню
                return "menu"
            elif result == "next_level":  # Перемога → наступний рівень
                return "next_level"

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
        time_text = pygame.font.SysFont("comicsans", 44).render(f"Level {self.level_number} - Time: {self.game_info.get_time()}s", 1, (255, 255, 255))
        self.win.blit(time_text, (10, self.level.height - 75))
        self.car.draw(self.win)
        pygame.display.update()
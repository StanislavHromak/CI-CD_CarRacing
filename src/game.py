import pygame
from src import level as l
from src import game_info as gi
from src import settings as st
from src import settings_menu as stm
from src import records as r
from src import car, collision as cl
from src import menu as mn
from src.utils import blit_text_center

class Game:
    """
    Клас, що керує основним циклом гри, меню, рівнями, налаштуваннями та рекордами.
    """
    def __init__(self):
        """
        Ініціалізує об’єкт гри з базовими параметрами та компонентами.
        """
        self.car = None
        self.game_info = None
        self.level = None
        pygame.font.init()
        self.running = True
        self.fps = 60
        self.level_number = 1
        self.settings = st.Settings()
        self.width, self.height = 800, 600
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.menu = mn.Menu(self.win, self.width, self.height)
        self.settings_menu = stm.SettingsMenu(self.win, self.width, self.height, self.settings)
        self.records = r.Records()

    def run(self):
        """
        Запускає основний цикл гри, що обробляє вибір користувача з меню
        та перенаправляє на відповідні функції (або виходить з програми)
        """
        while self.running:
            selected_option = self.show_menu()
            if selected_option == 0:  # Почати гру
                self.play_levels()
            elif selected_option == 1:  # Налаштування
                self.show_settings()
            elif selected_option == 2:  # Переглянути рекорд
                self.show_records()
            elif selected_option == 3:  # Вихід
                self.running = False

        pygame.quit()

    def show_settings(self):
        """
        Відкриває меню налаштувань гри
        """
        self.settings_menu.run() # Додано до налаштувань

    def show_menu(self):
        """
        Відображає головне меню та повертає вибір користувача.
        :return: Індекс обраного пункту меню (0-3) або None при закритті вікна.
        """
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
        """
        Керує проходженням усіх рівнів гри (1–5).
        Цикл завершується при поверненні в меню або після проходження всіх рівнів.
        """
        while self.level_number <= 5:
            result = self.play_level()
            if result == "menu":  # Якщо гравець програв, повертаємось у меню
                break
            self.level_number += 1
        self.level_number = 1  # Після завершення повертаємося в меню

    def play_level(self):
        """
        Керує одним рівнем гри (рухом машини, зіткненнями та переходом до наступного рівня).
        :return: "menu" при програші, "next_level" при проходженні рівня.
        """
        self.level = l.Level()
        self.game_info = gi.GameInfo()
        car_image_path = f"imgs/{self.settings.car_color}-car.png"
        self.car = car.Car(6, 4, car_image_path)
        self.win = pygame.display.set_mode((self.level.width, self.level.height))
        pygame.display.set_caption(f"Car Racing")
        clock = pygame.time.Clock()

        self.settings.reset_lives()

        while self.running:
            clock.tick(self.fps)
            self.handle_events()

            if not self.game_info.started:
                self.draw()
                blit_text_center(self.win, pygame.font.SysFont("arial", 40),
                                 "Натисніть на будь-яку клавішу для старту!", (255, 255, 0))
                pygame.display.update()
                continue

            self.car.move()
            result = cl.Collision.handle_collision(self.car, self.game_info, self.level, self.win,
                                               pygame.font.SysFont("arial", 40, bold=True),
                                               self.settings.lives, self.settings.difficulty)

            if isinstance(result, int):  # Якщо повернуто число (оновлені життя)
                self.settings.lives = result
            elif result == "menu":
                return "menu"
            elif isinstance(result, tuple) and result[0] == "next_level":  # Обробка кортежу
                level_time = result[1]  # Отримуємо час із кортежу
                self.records.update_records(self.level_number, level_time)
                return "next_level"

            self.draw()

    def show_records(self):
        """
        Відображає екран із рекордами гри.
        Показує найвищий пройдений рівень і найкращі часи для кожного рівня (1–5).
        """
        font = pygame.font.SysFont("times", 44)
        running = True
        while running:
            self.win.fill((0, 0, 0))
            record_info = self.records.get_record_info()
            if not record_info:
                text = font.render("Рекордів ще немає!", True, (255, 255, 255))
                self.win.blit(text,
                              (self.width // 2 - text.get_width() // 2,
                               self.height // 2 - text.get_height() // 2))
            else:
                level_text = font.render(f"Найвищий пройдений рівень: {record_info['level']}",
                                         True, (255, 255, 255))
                self.win.blit(level_text,
                              (self.width // 2 - level_text.get_width() // 2, self.height // 2 - 200))

                # Відображаємо найкращі часи для кожного рівня
                for i in range(1, 6):
                    time_text = font.render(f"Рівень {i}: {record_info['best_times'][i]}s",
                                            True, (255, 255, 255))
                    self.win.blit(time_text,
                                  (self.width // 2 - time_text.get_width() // 2,
                                   self.height // 2 - 100 + (i - 1) * 50))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False

    def handle_events(self):
        """
        Обробляє події Pygame (закриття вікна, зміна розміру, натискання клавіш).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.width, self.height = event.w, event.h
                self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                self.menu.width, self.menu.height = self.width, self.height
                self.settings_menu.width, self.settings_menu.height = self.width, self.height
                if self.level:
                    self.level.update_size(self.width, self.height)
            elif event.type == pygame.KEYDOWN and not self.game_info.started:
                self.game_info.start_game()

        if self.game_info.started:
            keys = pygame.key.get_pressed()
            self.car.handle_movement(keys)

    def draw(self):
        """
        Малює поточний стан гри на екрані.
        Відображає рівень, машину та текстову інформацію (рівень, таймер, життя).
        """
        self.level.draw(self.win)

        font = pygame.font.SysFont("times", 30)

        level_text = font.render(f"Рівень {self.level_number}", 1, (255, 255, 0))
        timer_text = font.render(f"Таймер: {self.game_info.get_time()}s", 1, (255, 255, 0))
        lives_text = font.render(f"Кількість життів: {self.settings.lives}", 1, (255, 255, 0))

        self.win.blit(level_text, (10, 600))
        self.win.blit(timer_text, (10, 640))
        self.win.blit(lives_text, (10, 680))

        self.car.draw(self.win)
        pygame.display.update()
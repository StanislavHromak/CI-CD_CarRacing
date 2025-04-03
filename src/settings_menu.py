import pygame

class SettingsMenu:
    """
    Клас для відображення та керування пунктом меню "Налаштування".
    """
    def __init__(self, win, width, height, settings):
        """
        Ініціалізує об’єкт меню налаштувань із заданими параметрами.
        :param win: Вікно Pygame для відображення.
        :param width: Ширина вікна.
        :param height: Висота вікна.
        :param settings: Екземпляр налаштувань гри для зміни кольору та складності.
        """
        self.win = win
        self.width = width
        self.height = height
        self.settings = settings
        self.font = pygame.font.SysFont("times", 40)
        self.options = ["Червоний", "Білий", "Фіолетовий", "Сірий", "Зелений"] # Кольори машин
        self.difficulties = ["Простий", "Середній", "Складний"] # Рівні складностей

        # Зворотне відображення для кольорів
        self.color_mapping = {
            "red": "Червоний",
            "white": "Білий",
            "purple": "Фіолетовий",
            "grey": "Сірий",
            "green": "Зелений"
        }

        # Ініціалізація поточного кольору
        current_color_ua = self.color_mapping.get(self.settings.car_color, "Червоний")
        self.selected_color = self.options.index(current_color_ua)

        # Ініціалізація поточної складності
        current_difficulty = self.settings.difficulty.capitalize()
        self.selected_difficulty = self.difficulties.index(
            current_difficulty if current_difficulty in self.difficulties else "Складний")

        self.selected_item = 0

    def run(self):
        """
        Запускає цикл меню налаштувань для обробки введення користувача.
        Дозволяє переміщатися по пунктах меню, змінювати вибір і зберігати налаштування.
        Завершується при натисканні будь-якої клавіші, зберігаючи зміни лише при виборі 'Зберегти'.
        """
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_item = (self.selected_item + 1) % 3
                    elif event.key == pygame.K_UP:
                        self.selected_item = (self.selected_item - 1) % 3
                    elif event.key == pygame.K_LEFT:
                        if self.selected_item == 0:
                            self.selected_color = (self.selected_color - 1) % len(self.options)
                        elif self.selected_item == 1:
                            self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)
                    elif event.key == pygame.K_RIGHT:
                        if self.selected_item == 0:
                            self.selected_color = (self.selected_color + 1) % len(self.options)
                        elif self.selected_item == 1:
                            self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)
                    elif event.key == pygame.K_RETURN and self.selected_item == 2:  # Зберегти при Enter
                        self.settings.set_car_color(self.options[self.selected_color])
                        self.settings.set_difficulty(self.difficulties[self.selected_difficulty])
                        running = False
                    else:
                        running = False

    def draw(self):
        """
        Малює меню налаштувань на екрані.
        Відображає пункти для вибору кольору машини, рівня складності та кнопку 'Зберегти',
        виділяючи активний пункт жовтим кольором.
        """
        self.win.fill((0, 0, 0))

        color_text = self.font.render(f"Колір машини: {self.options[self.selected_color]}", True,
                                      (255, 255, 0) if self.selected_item == 0 else (255, 255, 255))
        difficulty_text = self.font.render(f"Рівень складності: {self.difficulties[self.selected_difficulty]}", True,
                                           (255, 255, 0) if self.selected_item == 1 else (255, 255, 255))
        save_text = self.font.render("Зберегти", True,
                                     (255, 255, 0) if self.selected_item == 2 else (255, 255, 255))

        self.win.blit(color_text, (self.width // 2 - 150, 200))
        self.win.blit(difficulty_text, (self.width // 2 - 150, 300))
        self.win.blit(save_text, (self.width // 2 - 50, 400))
        pygame.display.update()
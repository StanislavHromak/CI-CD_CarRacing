import pygame

class SettingsMenu:
    def __init__(self, win, width, height, settings):
        self.win = win
        self.width = width
        self.height = height
        self.settings = settings
        self.font = pygame.font.SysFont("comicsans", 40)
        self.options = ["Червоний", "Білий", "Фіолетовий", "Сірий", "Зелений"]
        self.difficulties = ["Простий", "Середній", "Складний"]

        # Зворотне відображення для кольорів
        self.color_mapping = {
            "red": "Червоний",
            "white": "Білий",
            "purple": "Фіолетовий",
            "grey": "Сірий",
            "green": "Зелений"
        }

        # Ініціалізація поточного кольору
        current_color_ua = self.color_mapping.get(self.settings.car_color, "Червоний")  # За замовчуванням "Червоний"
        self.selected_color = self.options.index(current_color_ua)

        # Ініціалізація поточної складності
        current_difficulty = self.settings.difficulty.capitalize()
        self.selected_difficulty = self.difficulties.index(
            current_difficulty if current_difficulty in self.difficulties else "Складний")

        self.selected_item = 0  # 0 - колір, 1 - складність, 2 - зберегти

    def run(self):
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_item = (self.selected_item + 1) % 3  # 3 елементи: колір, складність, зберегти
                    elif event.key == pygame.K_UP:
                        self.selected_item = (self.selected_item - 1) % 3
                    elif event.key == pygame.K_LEFT:
                        if self.selected_item == 0:  # Колір
                            self.selected_color = (self.selected_color - 1) % len(self.options)
                        elif self.selected_item == 1:  # Складність
                            self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)
                    elif event.key == pygame.K_RIGHT:
                        if self.selected_item == 0:  # Колір
                            self.selected_color = (self.selected_color + 1) % len(self.options)
                        elif self.selected_item == 1:  # Складність
                            self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_item == 2:  # Зберегти
                            self.settings.set_car_color(self.options[self.selected_color])
                            self.settings.set_difficulty(self.difficulties[self.selected_difficulty])
                            running = False  # Автоматично виходимо до меню
                        elif self.selected_item == 0:  # Колір
                            self.settings.set_car_color(self.options[self.selected_color])
                        elif self.selected_item == 1:  # Складність
                            self.settings.set_difficulty(self.difficulties[self.selected_difficulty])

    def draw(self):
        self.win.fill((0, 0, 0))
        # Колір машини
        color_text = self.font.render(f"Колір машини: {self.options[self.selected_color]}", True,
                                      (255, 255, 0) if self.selected_item == 0 else (255, 255, 255))
        # Рівень складності
        difficulty_text = self.font.render(f"Рівень складності: {self.difficulties[self.selected_difficulty]}", True,
                                           (255, 255, 0) if self.selected_item == 1 else (255, 255, 255))
        # Кнопка збереження
        save_text = self.font.render("Зберегти", True,
                                     (255, 255, 0) if self.selected_item == 2 else (255, 255, 255))

        self.win.blit(color_text, (self.width // 2 - 150, 200))
        self.win.blit(difficulty_text, (self.width // 2 - 150, 300))
        self.win.blit(save_text, (self.width // 2 - 50, 400))
        pygame.display.update()
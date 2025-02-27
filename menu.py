import pygame
import time

class Menu:
    def init(self, win, width, height):
        self.win = win
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("comicsans", 50)
        self.buttons = [
            ("Почати гру", (self.width // 2, 200)),
            ("Налаштування", (self.width // 2, 300)),
            ("Переглянути рекорд", (self.width // 2, 400)),
            ("Вихід", (self.width // 2, 500))
        ]
        self.selected = 0  # Індекс обраної кнопки

    def draw(self):
        self.win.fill((0, 0, 0))  # Чорний фон
        for i, (text, pos) in enumerate(self.buttons):
            color = (255, 255, 255) if i != self.selected else (255, 255, 0)  # Жовтий для обраної кнопки
            text_surf = self.font.render(text, True, color)
            text_rect = text_surf.get_rect(center=pos)
            self.win.blit(text_surf, text_rect)
        pygame.display.update()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.selected = (self.selected + 1) % len(self.buttons)
            time.sleep(0.2)  # Затримка, щоб не перескакувало швидко
        elif keys[pygame.K_UP]:
            self.selected = (self.selected - 1) % len(self.buttons)
            time.sleep(0.2)
        elif keys[pygame.K_RETURN]:
            return self.selected  # Повертає індекс обраної кнопки
        return None
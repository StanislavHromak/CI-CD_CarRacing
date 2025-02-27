import pygame
import time

class Menu:
    def __init__(self, win, width, height):
        self.win = win
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("times", 50)
        self.title_font = pygame.font.SysFont("arial", 70, bold=True)
        self.buttons = [
            ("Почати гру", (self.width // 2, 200)),
            ("Налаштування", (self.width // 2, 300)),
            ("Переглянути рекорд", (self.width // 2, 400)),
            ("Вихід", (self.width // 2, 500))
        ]
        self.selected = 0  # Індекс обраної кнопки

    def draw(self):
        self.win.fill((0, 0, 0))
        title_text = self.title_font.render("CAR RACING", True, (255, 0, 0))  # Білий колір
        title_rect = title_text.get_rect(center=(self.width // 2, 100))
        self.win.blit(title_text, title_rect)
        for i, (text, pos) in enumerate(self.buttons):
            color = (255, 255, 255) if i != self.selected else (255, 255, 0)
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
            return self.selected
        return None
import pygame

class Menu:
    def __init__(self, win, width, height):
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
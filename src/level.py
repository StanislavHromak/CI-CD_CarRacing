import pygame
from src.utils import scale_image

class Level:
    """
    Клас, що представляє рівень гри
    """
    def __init__(self):
        """
        Ініціалізує об’єкт рівня з масштабованими зображеннями та масками.
        """
        self.grass = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5) # Трава
        self.track = scale_image(pygame.image.load("imgs/track.png"), 800 / 900) # Траса
        self.track_border = scale_image(pygame.image.load("imgs/track-border.png"), 800 / 900) # Краї траси
        self.finish = pygame.image.load("imgs/finish.png") # фініш
        # Список зображень і їх позицій для відображення.
        self.images = [(self.grass, (0, 0)), (self.track, (0, 0)), (self.finish, (130, 250)),
                       (self.track_border, (0, 0))]
        self.track_border_mask = pygame.mask.from_surface(self.track_border) # Маска для країв траси
        self.finish_mask = pygame.mask.from_surface(self.finish) # Маска фінішу для виявлення проходження.
        self.width = self.track.get_width() # Ширина
        self.height = self.track.get_height() # Висота

    def draw(self, win):
        """
        Малює рівень на екрані.
        :param win: Вікно Pygame для відображення рівня.
        """
        for img, pos in self.images:
            win.blit(img, pos)
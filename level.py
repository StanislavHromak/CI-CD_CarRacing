import pygame
from utils import scale_image

class Level:
    def __init__(self):
        self.grass = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
        self.track = scale_image(pygame.image.load("imgs/track.png"), 800/900)
        self.track_border = scale_image(pygame.image.load("imgs/track-border.png"), 800/900)
        self.finish = pygame.image.load("imgs/finish.png")
        self.images = [(self.grass, (0, 0)), (self.track, (0, 0)), (self.finish, (130, 250)),
                       (self.track_border, (0, 0))]
        self.track_border_mask = pygame.mask.from_surface(self.track_border)
        self.finish_mask = pygame.mask.from_surface(self.finish)
        self.width = self.track.get_width()
        self.height = self.track.get_height()

    def draw(self, win):
        for img, pos in self.images:
            win.blit(img, pos)
import pygame
from utils import blit_text_center

class Collision:
    @staticmethod
    def handle_collision(player_car, game_info, level, win, font):
        # Використовуємо маски рівня без створення нового об'єкта
        if player_car.collide(level.track_border_mask):
            blit_text_center(win, font, "You lost! Try again.")
            pygame.display.update()
            pygame.time.wait(1500)
            game_info.started = False
            player_car.reset()

        if player_car.collide(level.finish_mask, 130, 250):
            blit_text_center(win, font, "You won! Congratulations!")
            pygame.display.update()
            pygame.time.wait(1500)
            game_info.started = False
            player_car.reset()
import pygame
from utils import blit_text_center

class Collision:
    @staticmethod
    def handle_collision(player_car, game_info, level, win, font, lives, difficulty):
        if player_car.collide(level.track_border_mask):
            lives -= 1
            if difficulty == "складний" or lives <= 0:
                blit_text_center(win, font, "ВИ ПРОГРАЛИ! СПРОБУЙТЕ ЗНОВУ!", (255, 0, 0))
                pygame.display.update()
                pygame.time.wait(1500)
                game_info.started = False
                player_car.reset()
                return "menu"
            else:
                player_car.reset()
                return lives

        if player_car.collide(level.finish_mask, 130, 250):
            level_time = game_info.get_time()  # Отримуємо час перед затримкою
            blit_text_center(win, font, "ВИ ВИГРАЛИ! ВІТАЄМО!", (0, 255, 0))
            pygame.display.update()
            pygame.time.wait(1500)
            player_car.reset()
            return "next_level", level_time  # Повертаємо час разом із результатом
        return lives
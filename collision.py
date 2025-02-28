import pygame
import math
from utils import blit_text_center

class Collision:
    """
    Клас обробки зіткнення машини із краєм траси і фінішем
    """
    @staticmethod
    def handle_collision(player_car, game_info, level, win, font, lives, difficulty):
        """
        Обробляє зіткнення машини з межами траси та фінішем.
        :param player_car: Екземпляр машини гравця.
        :param game_info: Інформація про стан гри.
        :param level: Поточний рівень гри.
        :param win: Вікно Pygame для відображення.
        :param font: Шрифт для тексту.
        :param lives: Кількість життів гравця.
        :param difficulty: Рівень складності гри.
        :return: "menu" при програші, кількість життів при зіткненні,
        ("next_level", level_time) при досягненні фінішу.
        """
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
                # Злегка зміщуємо позицію машини
                current_x, current_y = player_car.x, player_car.y
                new_x = current_x + 10 * math.sin(math.radians(player_car.angle))
                new_y = current_y + 10 * math.cos(math.radians(player_car.angle))
                player_car.reset(new_x, new_y)
                return lives

        if player_car.collide(level.finish_mask, 130, 250):
            level_time = game_info.get_time()
            blit_text_center(win, font, "ВИ ВИГРАЛИ! ВІТАЄМО!", (0, 255, 0))
            pygame.display.update()
            pygame.time.wait(1500)
            player_car.reset()
            return "next_level", level_time
        return lives
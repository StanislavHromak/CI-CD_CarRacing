import pygame
from utils import blit_text_center

class Collision:
    @staticmethod
    def handle_collision(player_car, game_info, level, win, font, lives, difficulty):
        if player_car.collide(level.track_border_mask):
            lives -= 1
            if difficulty == "складний" or lives <= 0:
                # На складному рівні або якщо життя закінчилися — завершуємо гру
                blit_text_center(win, font, "You lost! Try again.")
                pygame.display.update()
                pygame.time.wait(1500)
                game_info.started = False
                player_car.reset()
                return "menu"
            else:
                # На простому або середньому рівні — скидаємо позицію машини і продовжуємо
                player_car.reset()
                return lives  # Повертаємо оновлену кількість життів

        if player_car.collide(level.finish_mask, 130, 250):
            blit_text_center(win, font, "You won! Congratulations!")
            pygame.display.update()
            pygame.time.wait(1500)
            game_info.started = False
            player_car.reset()
            return "next_level"
        return lives  # Повертаємо оновлену кількість життів
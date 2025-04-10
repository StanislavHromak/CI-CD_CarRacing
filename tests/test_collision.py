from unittest.mock import Mock, patch
from src.collision import Collision

class TestCollision:
    @patch("src.collision.blit_text_center")
    @patch("pygame.display.update")
    @patch("pygame.time.wait")
    def test_collision_with_border_game_over(self, mock_wait, mock_update, mock_blit):
        # Підготовка моків
        player_car = Mock()
        player_car.collide.side_effect = [True]  # Створити зіткнення з межами
        game_info = Mock()
        game_info.started = True
        level = Mock()
        level.track_border_mask = Mock()
        win = Mock()
        font = Mock()
        lives = 1
        difficulty = "складний"

        # Виклик
        result = Collision.handle_collision(player_car, game_info, level, win, font, lives, difficulty)

        # Перевірка
        mock_blit.assert_called_once()
        mock_update.assert_called_once()
        mock_wait.assert_called_once()
        player_car.reset.assert_called_once()
        assert result == "menu"
        assert game_info.started is False

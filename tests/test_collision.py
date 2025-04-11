from unittest.mock import Mock, patch
from src.collision import Collision


class TestCollision:
    """
    Клас для тестування функціональності класу Collision.
    Перевіряє обробку зіткнень машини з межами траси та фінішем.
    """
    @patch("src.collision.blit_text_center")
    @patch("pygame.display.update")
    @patch("pygame.time.wait")
    def test_collision_with_border_game_over(self, mock_wait, mock_update, mock_blit):
        """
        Перевіряє зіткнення з межами траси, що призводить до програшу.
        Очікує відображення повідомлення про програш і повернення до меню.
        :param mock_wait: Замоканий метод pygame.time.wait.
        :param mock_update: Замоканий метод pygame.display.update.
        :param mock_blit: Замоканий метод blit_text_center.
        """
        # Підготовка моків
        player_car = Mock()
        player_car.collide.side_effect = [True]  # Зіткнення з межами
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

    @patch("pygame.display.update")
    @patch("pygame.time.wait")
    def test_collision_with_border_not_game_over(self, mock_wait, mock_update):
        """
        Перевіряє зіткнення з межами траси, що не призводить до програшу.
        Очікує зменшення кількості життів і скидання позиції машини.
        :param mock_wait: Замоканий метод pygame.time.wait.
        :param mock_update: Замоканий метод pygame.display.update.
        """
        player_car = Mock()
        player_car.collide.side_effect = [True]  # Зіткнення з межами
        player_car.x = 100
        player_car.y = 200
        player_car.angle = 90
        game_info = Mock()
        level = Mock()
        level.track_border_mask = Mock()
        win = Mock()
        font = Mock()
        lives = 2
        difficulty = "легкий"

        result = Collision.handle_collision(player_car, game_info, level, win, font, lives, difficulty)

        player_car.reset.assert_called_once()
        assert isinstance(result, int)
        assert result == 1  # lives - 1

    @patch("src.collision.blit_text_center")
    @patch("pygame.display.update")
    @patch("pygame.time.wait")
    def test_collision_with_finish(self, mock_wait, mock_update, mock_blit):
        """
        Перевіряє зіткнення з фінішем.
        Очікує відображення повідомлення про перемогу і повернення кортежу ("next_level", час).
        :param mock_wait: Замоканий метод pygame.time.wait.
        :param mock_update: Замоканий метод pygame.display.update.
        :param mock_blit: Замоканий метод blit_text_center.
        """
        player_car = Mock()
        player_car.collide.side_effect = [False, True]  # Нема зіткнення з межами, але є з фінішем
        game_info = Mock()
        game_info.get_time.return_value = 42.0
        level = Mock()
        level.track_border_mask = Mock()
        level.finish_mask = Mock()
        win = Mock()
        font = Mock()
        lives = 3
        difficulty = "середній"

        result = Collision.handle_collision(player_car, game_info, level, win, font, lives, difficulty)

        mock_blit.assert_called_once()
        mock_update.assert_called_once()
        mock_wait.assert_called_once()
        player_car.reset.assert_called_once()
        assert result == ("next_level", 42.0)

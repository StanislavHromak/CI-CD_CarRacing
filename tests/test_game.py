import pytest
import pygame
from unittest.mock import patch, MagicMock
from src.game import Game


@pytest.fixture
def game():
    """
    Створює екземпляр гри для тестування з замоканими залежностями Pygame.
    :return: Створює екземпляр класу Game
    """
    with patch('pygame.display.set_mode'), \
         patch('pygame.font.SysFont'), \
         patch('pygame.display.set_caption'):
        return Game()


@pytest.fixture(autouse=True)
def disable_pygame_display(monkeypatch):
    """
    Вимикає функції відображення Pygame для тестування.
    Замінює методи set_mode, set_caption і update на замокані версії.
    :param monkeypatch: Об’єкт pytest для заміни атрибутів Pygame.
    """
    monkeypatch.setattr(pygame.display, "set_mode", lambda *args, **kwargs: MagicMock())
    monkeypatch.setattr(pygame.display, "set_caption", lambda *args, **kwargs: None)
    monkeypatch.setattr(pygame.display, "update", lambda: None)


class TestGame:
    """
    Клас для тестування функціональності класу Game.
    """
    def test_init(self, game):
        """
        Перевіряє початкову ініціалізацію об’єкта гри.
        Очікує, що налаштування створено, гра запущена, а початковий рівень дорівнює 1.
        :param game: Екземпляр класу Game для тестування.
        """
        assert isinstance(game.settings, object)
        assert game.running is True
        assert game.level_number == 1

    def test_run(self, game, monkeypatch):
        """
        Перевіряє основний цикл гри з вибором виходу з меню.
        Очікує завершення гри після вибору опції "Вихід".
        :param game: Екземпляр класу Game для тестування.
        :param monkeypatch: Об’єкт pytest для заміни атрибутів Pygame.
        """
        game.show_menu = MagicMock(return_value=3)  # "Вихід"
        monkeypatch.setattr(pygame, "quit", MagicMock())

        game.run()

        assert game.running is False

    def test_play_levels_menu_exit(self, game):
        """
        Перевіряє повернення до меню після програшу на рівні.
        Очікує, що номер рівня скинеться до 1.
        :param game: Екземпляр класу Game для тестування.
        """
        game.play_level = MagicMock(return_value="menu")
        game.level_number = 1
        game.play_levels()
        assert game.level_number == 1

    def test_play_levels_pass_all_levels(self, game):
        """
        Перевіряє проходження всіх рівнів гри.
        Очікує, що після завершення всіх рівнів номер рівня скинеться до 1.
        :param game: Екземпляр класу Game для тестування.
        """
        game.play_level = MagicMock(return_value="next_level")
        game.level_number = 1
        game.play_levels()
        assert game.level_number == 1

    @patch("src.game.car.Car")
    @patch("src.game.l.Level")
    @patch("src.game.gi.GameInfo")
    @patch("src.game.cl.Collision.handle_collision")
    @patch("src.game.pygame.display.set_mode", return_value=MagicMock())
    @patch("src.game.pygame.font.SysFont", return_value=MagicMock(render=MagicMock()))
    def test_play_level_next_level(self, mock_font, mock_display, mock_collision, mock_game_info_class,
                                   mock_level_class, mock_car_class, game):
        """
        Перевіряє проходження одного рівня з результатом "next_level".
        Очікує, що гра обробляє зіткнення та повертає правильний результат.
        :param mock_font: Замоканий об’єкт шрифту Pygame.
        :param mock_display: Замоканий об’єкт дисплея Pygame.
        :param mock_collision: Замоканий метод обробки зіткнень.
        :param mock_game_info_class: Замоканий клас GameInfo.
        :param mock_level_class: Замоканий клас Level.
        :param mock_car_class: Замоканий клас Car.
        :param game: Екземпляр класу Game для тестування.
        """
        game.running = True
        game.handle_events = MagicMock()
        game.draw = MagicMock()

        mock_game_info = MagicMock()
        mock_game_info.started = True
        mock_game_info.get_time.return_value = 10
        mock_game_info_class.return_value = mock_game_info

        mock_collision.return_value = ("next_level", 10)

        def fake_tick(val):
            game.running = False

        mock_clock = MagicMock()
        mock_clock.tick.side_effect = fake_tick

        with patch("src.game.pygame.time.Clock", return_value=mock_clock):
            result = game.play_level()

        assert result == "next_level"
        mock_collision.assert_called()

    @patch('pygame.event.get', return_value=[])
    def test_show_menu_returns_selected(self, mock_event, game):
        """
        Перевіряє вибір опції в меню.
        Очікує повернення обраного значення (наприклад, 2).
        :param mock_event: Замоканий об’єкт подій Pygame.
        :param game: Екземпляр класу Game для тестування.
        """
        game.menu.draw = MagicMock()
        game.menu.handle_input = MagicMock(return_value=2)
        assert game.show_menu() == 2

    @patch('pygame.event.get', return_value=[MagicMock(type=pygame.QUIT)])
    def test_show_menu_handles_quit(self, mock_event, game):
        """
        Перевіряє обробку закриття вікна в меню.
        Очікує, що гра завершується і повертається None.
        :param mock_event: Замоканий об’єкт подій Pygame.
        :param game: Екземпляр класу Game для тестування.
        """
        game.menu.draw = MagicMock()
        game.menu.handle_input = MagicMock(return_value=None)
        result = game.show_menu()
        assert result is None
        assert not game.running

    def test_show_settings_runs_menu(self, game):
        """
        Перевіряє запуск меню налаштувань.
        Очікує, що метод run викликається один раз.
        :param game: Екземпляр класу Game для тестування.
        """
        game.settings_menu.run = MagicMock()
        game.show_settings()
        game.settings_menu.run.assert_called_once()

    @patch('pygame.event.get', return_value=[])
    def test_show_records_no_records(self, mock_event, game):
        """
        Перевіряє відображення екрана рекордів, коли рекордів немає.
        Очікує, що викликається метод отримання інформації про рекорди.
        :param mock_event: Замоканий об’єкт подій Pygame.
        :param game: Екземпляр класу Game для тестування.
        """
        game.records.get_record_info = MagicMock(return_value=None)
        game.win = MagicMock()
        font_mock = MagicMock()
        text_mock = MagicMock()
        text_mock.get_width.return_value = 100
        text_mock.get_height.return_value = 50
        font_mock.render.return_value = text_mock

        with patch('pygame.font.SysFont', return_value=font_mock):
            with patch('pygame.display.update'):
                event = MagicMock()
                event.type = pygame.KEYDOWN
                mock_event.return_value = [event]
                game.show_records()

        assert game.records.get_record_info.called

    def test_handle_events_quit(self, monkeypatch, game):
        """
        Перевіряє обробку події закриття вікна.
        Очікує, що гра завершується після події QUIT.
        :param monkeypatch: Об’єкт pytest для заміни атрибутів Pygame.
        :param game: Екземпляр класу Game для тестування.
        """
        event = MagicMock()
        event.type = pygame.QUIT
        monkeypatch.setattr(pygame.event, "get", lambda: [event])

        game.game_info = MagicMock()
        game.game_info.started = False

        game.handle_events()
        assert not game.running

    def test_handle_events_resize(self, monkeypatch, game):
        """
        Перевіряє обробку зміни розміру вікна.
        Очікує, що розміри гри оновлюються, а рівень змінює розмір.
        :param monkeypatch: Об’єкт pytest для заміни атрибутів Pygame.
        :param game: Екземпляр класу Game для тестування.
        """
        event = MagicMock()
        event.type = pygame.VIDEORESIZE
        event.w = 1024
        event.h = 768

        game.level = MagicMock()
        game.game_info = MagicMock()
        game.game_info.started = False

        monkeypatch.setattr(pygame.event, "get", lambda: [event])
        monkeypatch.setattr(pygame.display, "set_mode", lambda *a, **k: MagicMock())

        game.handle_events()

        assert game.width == 1024
        assert game.height == 768
        game.level.update_size.assert_called_once_with(1024, 768)

    def test_draw(self, game):
        """
        Перевіряє малювання поточного стану гри.
        Очікує, що викликаються методи малювання рівня та машини.
        :param game: Екземпляр класу Game для тестування.
        """
        game.level = MagicMock()
        game.car = MagicMock()
        game.game_info = MagicMock()
        game.game_info.get_time.return_value = 12
        game.settings.lives = 3
        game.level_number = 2
        game.win = MagicMock()

        with patch("pygame.font.SysFont", return_value=MagicMock(render=MagicMock(get_width=lambda: 0, get_height=lambda: 0))), \
             patch("pygame.display.update"):
            game.draw()

        game.level.draw.assert_called_once()
        game.car.draw.assert_called_once()
import pytest
import pygame
from unittest.mock import patch, MagicMock
from src.game import Game


@pytest.fixture
def game():
    with patch('pygame.display.set_mode'), \
         patch('pygame.font.SysFont'), \
         patch('pygame.display.set_caption'):
        return Game()


@pytest.fixture(autouse=True)
def disable_pygame_display(monkeypatch):
    monkeypatch.setattr(pygame.display, "set_mode", lambda *args, **kwargs: MagicMock())
    monkeypatch.setattr(pygame.display, "set_caption", lambda *args, **kwargs: None)
    monkeypatch.setattr(pygame.display, "update", lambda: None)


class TestGame:
    def test_init(self, game):
        assert isinstance(game.settings, object)
        assert game.running is True
        assert game.level_number == 1

    def test_run(self, game, monkeypatch):
        game.show_menu = MagicMock(return_value=3)  # "Вихід"
        monkeypatch.setattr(pygame, "quit", MagicMock())

        game.run()

        assert game.running is False

    def test_play_levels_menu_exit(self, game):
        game.play_level = MagicMock(return_value="menu")
        game.level_number = 1

        game.play_levels()

        assert game.level_number == 1

    def test_play_levels_pass_all_levels(self, game):
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

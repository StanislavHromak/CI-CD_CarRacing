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

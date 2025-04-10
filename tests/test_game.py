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

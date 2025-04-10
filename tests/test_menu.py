import pytest
import pygame
from unittest.mock import patch, MagicMock
from src.menu import Menu

# Фейковий об'єкт для імітації натиснутої клавіші
class FakeKeyPress:
    def __init__(self, pressed_key=None):
        self.pressed_key = pressed_key

    def __getitem__(self, key):
        return key == self.pressed_key

@pytest.fixture
def mock_menu():
    pygame.init()
    win = MagicMock()
    menu = Menu(win, 800, 600)
    return menu
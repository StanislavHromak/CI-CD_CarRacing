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


class TestMenu:
    def test_initialization(self, mock_menu):
        assert mock_menu.width == 800
        assert mock_menu.height == 600
        assert len(mock_menu.buttons) == 4
        assert mock_menu.selected == 0

    @patch("src.menu.time.sleep")
    @patch("src.menu.pygame.key.get_pressed")
    def test_handle_input_down_key(self, mock_keys, mock_sleep, mock_menu):
        mock_keys.return_value = FakeKeyPress(pygame.K_DOWN)
        prev = mock_menu.selected
        mock_menu.handle_input()
        assert mock_menu.selected == (prev + 1) % len(mock_menu.buttons)

    @patch("src.menu.time.sleep")
    @patch("src.menu.pygame.key.get_pressed")
    def test_handle_input_up_key(self, mock_keys, mock_sleep, mock_menu):
        mock_keys.return_value = FakeKeyPress(pygame.K_UP)
        prev = mock_menu.selected
        mock_menu.handle_input()
        assert mock_menu.selected == (prev - 1) % len(mock_menu.buttons)

    @patch("src.menu.pygame.key.get_pressed")
    def test_handle_input_enter_key(self, mock_keys, mock_menu):
        mock_keys.return_value = FakeKeyPress(pygame.K_RETURN)
        result = mock_menu.handle_input()
        assert result == mock_menu.selected

    @patch("src.menu.pygame.key.get_pressed")
    def test_handle_input_nothing_pressed(self, mock_keys, mock_menu):
        mock_keys.return_value = FakeKeyPress()
        result = mock_menu.handle_input()
        assert result is None
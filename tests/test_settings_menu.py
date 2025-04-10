import unittest
from unittest.mock import MagicMock, patch
import pygame
from src.settings_menu import SettingsMenu
from src.settings import Settings


class TestSettingsMenu(unittest.TestCase):
    @patch('pygame.font.SysFont')  # Мокаємо pygame.font.SysFont, щоб не ініціалізувати реальний шрифт
    def setUp(self, mock_font):
        """Ініціалізуємо об'єкти перед кожним тестом."""
        # Ініціалізація об'єктів для тесту
        self.win = MagicMock()  # Мокаємо вікно
        self.width = 800
        self.height = 600
        self.settings = Settings()  # Ініціалізація налаштувань
        mock_font.return_value = MagicMock()  # Мокаємо шрифт
        self.menu = SettingsMenu(self.win, self.width, self.height, self.settings)

    def test_initial_state(self):
        """Перевіряємо початкові налаштування меню."""
        self.assertEqual(self.menu.selected_color, 0)  # Початковий колір - Червоний
        self.assertEqual(self.menu.selected_difficulty, 2)  # Початковий рівень складності - Складний
        self.assertEqual(self.menu.selected_item, 0)  # Початково вибраний елемент - колір

    def test_handle_input_up(self):
        """Перевіряємо обробку введення при натисканні клавіші 'UP'."""
        self.menu.selected_item = 1  # Початково вибраний елемент - рівень складності
        with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)]):
            continue_running = self.menu.handle_input()
            self.assertEqual(self.menu.selected_item, 0)  # Повинно переміститися на колір машини

    def test_handle_input_down(self):
        """Перевіряємо обробку введення при натисканні клавіші 'DOWN'."""
        self.menu.selected_item = 0  # Початково вибраний елемент - колір
        with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)]):
            continue_running = self.menu.handle_input()
            self.assertEqual(self.menu.selected_item, 1)  # Повинно переміститися на рівень складності
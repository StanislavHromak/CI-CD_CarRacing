import unittest
from unittest.mock import MagicMock, patch
import pygame
from src.settings_menu import SettingsMenu
from src.settings import Settings


class TestSettingsMenu(unittest.TestCase):
    @patch('pygame.font.SysFont')
    def setUp(self, mock_font):
        """
        Ініціалізує об'єкти перед кожним тестом
        :param mock_font: Замокований шрифт
        """
        self.win = MagicMock()  # Мокаємо вікно
        self.width = 800
        self.height = 600
        self.settings = Settings()
        mock_font.return_value = MagicMock()  # Мокаємо шрифт
        self.menu = SettingsMenu(self.win, self.width, self.height, self.settings)

    def test_initial_state(self):
        """
        Перевіряє початкові налаштування меню
        """
        self.assertEqual(self.menu.selected_color, 0)  # Початковий колір - Червоний
        self.assertEqual(self.menu.selected_difficulty, 2)  # Початковий рівень складності - Складний
        self.assertEqual(self.menu.selected_item, 0)  # Початково вибраний елемент - колір

    def test_handle_input_up(self):
        """
        Перевіряє обробку введення при натисканні клавіші 'UP'
        """
        self.menu.selected_item = 1  # Початково вибраний елемент - рівень складності
        with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)]):
            continue_running = self.menu.handle_input()
            self.assertEqual(self.menu.selected_item, 0)  # Повинно переміститися на колір машини

    def test_handle_input_down(self):
        """
        Перевіряє обробку введення при натисканні клавіші 'DOWN'
        """
        self.menu.selected_item = 0  # Початково вибраний елемент - колір
        with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)]):
            continue_running = self.menu.handle_input()
            self.assertEqual(self.menu.selected_item, 1)  # Повинно переміститися на рівень складності

    def test_handle_input_left_right(self):
        """
        Перевіряє обробку введення при натисканні клавіші 'LEFT' та 'RIGHT'
        """
        self.menu.selected_item = 0  # Початково вибраний елемент - колір
        self.menu.selected_color = 0  # Початково вибраний колір - Червоний

        with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)]):
            self.menu.handle_input()
            self.assertEqual(self.menu.selected_color, 4)  # Повинно перейти до останнього кольору (Зелений)

        with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)]):
            self.menu.handle_input()
            self.assertEqual(self.menu.selected_color, 0)  # Повинно перейти до першого кольору (Червоний)

    def test_save_settings(self):
        """
        Перевіряє збереження налаштувань при натисканні 'ENTER' на збереження
        """
        self.menu.selected_item = 2  # Вибрано пункт "Зберегти"
        self.menu.selected_color = 2  # Вибраний колір - Фіолетовий
        self.menu.selected_difficulty = 1  # Вибрано складність - Середній

        with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)]):
            continue_running = self.menu.handle_input()
            self.assertFalse(continue_running)  # Цикл має завершитись
            self.assertEqual(self.settings.car_color, "purple")  # Перевірка, що колір змінено на Фіолетовий
            self.assertEqual(self.settings.difficulty, "середній")  # Перевірка, що складність змінена на Середній

    def test_handle_quit(self):
        """
        Перевіряє, що при натисканні на кнопку 'QUIT' цикл завершиться
        """
        with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.QUIT)]):
            continue_running = self.menu.handle_input()
            self.assertFalse(continue_running)  # Цикл має завершитись

if __name__ == "__main__":
    unittest.main()
import pytest
import pygame
from unittest.mock import patch, MagicMock
from src.menu import Menu


class FakeKeyPress:
    """
    Фейковий об’єкт для імітації натиснутої клавіші.
    Використовується для тестування обробки введення користувача.
    """
    def __init__(self, pressed_key=None):
        """
        Ініціалізує об’єкт із заданою натиснутою клавішею.
        :param pressed_key: Клавіша, яка вважається натиснутою (за замовчуванням None).
        """
        self.pressed_key = pressed_key

    def __getitem__(self, key):
        """
        Перевіряє, чи збігається запитувана клавіша з натиснутою.
        :param key: Клавіша для перевірки.
        :return: True, якщо клавіша збігається з натиснутою, інакше False.
        """
        return key == self.pressed_key


@pytest.fixture
def mock_menu():
    """
    Створює екземпляр меню для тестування з замоканим вікном Pygame.
    :return: Екземпляр класу Menu.
    """
    pygame.init()
    win = MagicMock()
    menu = Menu(win, 800, 600)
    return menu


class TestMenu:
    """
    Клас для тестування функціональності класу Menu.
    Перевіряє ініціалізацію меню, обробку введення та відображення.
    """
    def test_initialization(self, mock_menu):
        """
        Перевіряє початкову ініціалізацію меню.
        Очікує правильні розміри, кількість кнопок і початковий вибір.
        :param mock_menu: Екземпляр класу Menu для тестування.
        """
        assert mock_menu.width == 800
        assert mock_menu.height == 600
        assert len(mock_menu.buttons) == 4
        assert mock_menu.selected == 0

    @patch("src.menu.time.sleep")
    @patch("src.menu.pygame.key.get_pressed")
    def test_handle_input_down_key(self, mock_keys, mock_sleep, mock_menu):
        """
        Перевіряє обробку натискання клавіші "Вниз".
        Очікує, що індекс обраної кнопки збільшується на 1 (з урахуванням циклічності).
        :param mock_keys: Замоканий метод pygame.key.get_pressed.
        :param mock_sleep: Замоканий метод time.sleep.
        :param mock_menu: Екземпляр класу Menu для тестування.
        """
        mock_keys.return_value = FakeKeyPress(pygame.K_DOWN)
        prev = mock_menu.selected
        mock_menu.handle_input()
        assert mock_menu.selected == (prev + 1) % len(mock_menu.buttons)

    @patch("src.menu.time.sleep")
    @patch("src.menu.pygame.key.get_pressed")
    def test_handle_input_up_key(self, mock_keys, mock_sleep, mock_menu):
        """
        Перевіряє обробку натискання клавіші "Вгору".
        Очікує, що індекс обраної кнопки зменшується на 1 (з урахуванням циклічності).
        :param mock_keys: Замоканий метод pygame.key.get_pressed.
        :param mock_sleep: Замоканий метод time.sleep.
        :param mock_menu: Екземпляр класу Menu для тестування.
        """
        mock_keys.return_value = FakeKeyPress(pygame.K_UP)
        prev = mock_menu.selected
        mock_menu.handle_input()
        assert mock_menu.selected == (prev - 1) % len(mock_menu.buttons)

    @patch("src.menu.pygame.key.get_pressed")
    def test_handle_input_enter_key(self, mock_keys, mock_menu):
        """
        Перевіряє обробку натискання клавіші "Enter".
        Очікує повернення індексу обраної кнопки.
        :param mock_keys: Замоканий метод pygame.key.get_pressed.
        :param mock_menu: Екземпляр класу Menu для тестування.
        """
        mock_keys.return_value = FakeKeyPress(pygame.K_RETURN)
        result = mock_menu.handle_input()
        assert result == mock_menu.selected

    @patch("src.menu.pygame.key.get_pressed")
    def test_handle_input_nothing_pressed(self, mock_keys, mock_menu):
        """
        Перевіряє обробку введення, коли жодна клавіша не натиснута.
        Очікує повернення None.
        :param mock_keys: Замоканий метод pygame.key.get_pressed.
        :param mock_menu: Екземпляр класу Menu для тестування.
        """
        mock_keys.return_value = FakeKeyPress()
        result = mock_menu.handle_input()
        assert result is None

    @patch("src.menu.pygame.display.update")
    @patch("src.menu.pygame.font.Font")
    def test_draw(self, mock_font_class, mock_display_update, mock_menu):
        """
        Перевіряє малювання меню на екрані.
        Очікує, що викликаються методи заповнення екрану, рендерингу тексту та оновлення дисплея.
        :param mock_font_class: Замоканий клас pygame.font.Font.
        :param mock_display_update: Замоканий метод pygame.display.update.
        :param mock_menu: Екземпляр класу Menu для тестування.
        """
        fake_surface = MagicMock()
        fake_surface.get_rect.return_value = MagicMock(center=(0, 0))

        mock_font = MagicMock()
        mock_font.render.return_value = fake_surface
        mock_font_class.return_value = mock_font

        # Вручну призначаємо замокані шрифти, бо вони створені у конструкторі
        mock_menu.font = mock_font
        mock_menu.title_font = mock_font

        mock_menu.draw()

        assert mock_menu.win.fill.called
        assert mock_font.render.call_count == len(mock_menu.buttons) + 1
        assert mock_menu.win.blit.call_count == len(mock_menu.buttons) + 1
        assert mock_display_update.called

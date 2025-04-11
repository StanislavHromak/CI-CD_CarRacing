import pytest
import pygame
from unittest.mock import patch, Mock
from src.level import Level


class TestLevel:
    """
    Клас для тестування функціональності класу Level.
    Перевіряє ініціалізацію рівня, створення зображень, масок та відображення.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Налаштовує тестове середовище перед кожним тестом.
        Ініціалізує Pygame і створює екземпляр Level з замоканими зображеннями.
        :return: Налаштоване середовище для тестування.
        """
        pygame.init()
        self.surface = pygame.Surface((100, 100))  # Поверхня для замоканих зображень

        with patch("src.level.pygame.image.load", return_value=self.surface), \
             patch("src.level.scale_image", return_value=self.surface):
            self.level = Level()
            yield

    def test_images_are_loaded_and_scaled(self):
        """
        Перевіряє, чи всі зображення рівня є об’єктами pygame.Surface.
        Очікує, що трава, траса, межі траси та фініш правильно ініціалізовані.
        """
        assert isinstance(self.level.grass, pygame.Surface)
        assert isinstance(self.level.track, pygame.Surface)
        assert isinstance(self.level.track_border, pygame.Surface)
        assert isinstance(self.level.finish, pygame.Surface)

    def test_images_list(self):
        """
        Перевіряє, чи список images містить правильні пари (зображення, позиція).
        Очікує, що список має 4 елементи, кожен із Surface та кортежем координат.
        """
        assert len(self.level.images) == 4
        for img, pos in self.level.images:
            assert isinstance(img, pygame.Surface)
            assert isinstance(pos, tuple)
            assert len(pos) == 2

    def test_masks_created(self):
        """
        Перевіряє створення масок для меж траси та фінішу.
        Очікує, що track_border_mask та finish_mask є об’єктами pygame.mask.Mask.
        """
        assert isinstance(self.level.track_border_mask, pygame.mask.Mask)
        assert isinstance(self.level.finish_mask, pygame.mask.Mask)

    def test_width_and_height(self):
        """
        Перевіряє, чи ширина та висота рівня відповідають розмірам траси.
        Очікує, що width і height дорівнюють розмірам зображення траси.
        """
        assert self.level.width == self.surface.get_width()
        assert self.level.height == self.surface.get_height()

    def test_draw_calls_blit(self):
        """
        Перевіряє виклик методу малювання рівня.
        Очікує, що метод blit викликається 4 рази з правильними зображеннями та позиціями.
        """
        # Створюємо мок-об'єкт замість вікна
        mock_win = Mock()
        self.level.draw(mock_win)
        assert mock_win.blit.call_count == 4

        # Перевіряємо, що blit викликався з правильними аргументами
        expected_calls = self.level.images
        for call_args, expected in zip(mock_win.blit.call_args_list, expected_calls):
            args, _ = call_args
            assert args[0] == expected[0]  # Зображення
            assert args[1] == expected[1]  # Позиція

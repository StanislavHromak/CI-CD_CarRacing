import pytest
import pygame
from unittest.mock import patch, Mock
from src.level import Level


class TestLevel:
    @pytest.fixture(autouse=True)
    def setup(self):
        pygame.init()
        self.surface = pygame.Surface((100, 100))

        with patch("src.level.pygame.image.load", return_value=self.surface), \
             patch("src.level.scale_image", return_value=self.surface):
            self.level = Level()
            yield

    def test_images_are_loaded_and_scaled(self):
        """
        Функція, що перевіряє, чи всі елементи - pygame.Surface
        """
        assert isinstance(self.level.grass, pygame.Surface)
        assert isinstance(self.level.track, pygame.Surface)
        assert isinstance(self.level.track_border, pygame.Surface)
        assert isinstance(self.level.finish, pygame.Surface)

    def test_images_list(self):
        """
        Функція, що перевіряє, чи images містить правильні пари (surface, position)
        """
        assert len(self.level.images) == 4
        for img, pos in self.level.images:
            assert isinstance(img, pygame.Surface)
            assert isinstance(pos, tuple)
            assert len(pos) == 2

    def test_masks_created(self):
        """
        Функція, що перевіряє створення масок
        """
        assert isinstance(self.level.track_border_mask, pygame.mask.Mask)
        assert isinstance(self.level.finish_mask, pygame.mask.Mask)

    def test_width_and_height(self):
        """
        Функція, яка перевіряє, чи рівень має ширину та висоту, як у track
        """
        assert self.level.width == self.surface.get_width()
        assert self.level.height == self.surface.get_height()

    def test_draw_calls_blit(self):
        # Створюємо мок-об'єкт замість вікна
        mock_win = Mock()
        self.level.draw(mock_win)
        assert mock_win.blit.call_count == 4

        # Перевіримо, що blit викликався з правильними аргументами
        expected_calls = self.level.images
        for call_args, expected in zip(mock_win.blit.call_args_list, expected_calls):
            args, _ = call_args
            assert args[0] == expected[0]  # зображення
            assert args[1] == expected[1]  # позиція
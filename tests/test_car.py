import pytest
import unittest
import pygame
from unittest.mock import patch, MagicMock
from src.car import Car

class TestCar(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup_car(self):
        pygame.init()
        # Створюємо справжній Surface
        real_surface = pygame.Surface((50, 50))

        with patch("src.car.pygame.image.load", return_value=real_surface), \
                patch("src.car.scale_image", return_value=real_surface), \
                patch("src.car.blit_rotate_center"):
            self.car = Car(max_vel=5, rotation_vel=5, image_path="some_path.png")
            yield

    def test_initial_state(self):
        assert self.car.x == 180
        assert self.car.y == 200
        assert self.car.vel == 0
        assert self.car.angle == 0
        assert self.car.max_vel == 5
        assert self.car.rotation_vel == 5






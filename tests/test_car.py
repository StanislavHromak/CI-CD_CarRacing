import pytest
import unittest
import pygame
from unittest.mock import patch, MagicMock
from src.car import Car

class TestCar(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup_car(self):
        pygame.init()
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

    def test_rotate_left(self):
        self.car.rotate(left=True)
        assert self.car.angle == 5

    def test_rotate_right(self):
        self.car.rotate(right=True)
        assert self.car.angle == -5

    def test_move_forward(self):
        self.car.angle = 0
        self.car.move_forward()
        assert self.car.vel == pytest.approx(0.05)
        assert self.car.y < 200  # бо рух вперед зменшує y

    def test_move_backward(self):
        self.car.angle = 0
        self.car.move_backward()
        assert self.car.vel == pytest.approx(-0.05)
        assert self.car.y > 200  # бо назад — y зростає

    def test_reduce_speed(self):
        self.car.vel = 1
        self.car.angle = 0
        self.car.reduce_speed()
        assert self.car.vel == pytest.approx(0.975)
        assert self.car.y < 200

    def test_reset_default(self):
        self.car.x, self.car.y, self.car.vel, self.car.angle = 100, 100, 3, 30
        self.car.reset()
        assert self.car.x == 180
        assert self.car.y == 200
        assert self.car.vel == 0
        assert self.car.angle == 0

    def test_reset_custom(self):
        self.car.reset(50, 60)
        assert self.car.x == 50
        assert self.car.y == 60
        assert self.car.angle == 0
        assert self.car.vel == 0

    def test_handle_movement_forward(self):
        keys = {
            pygame.K_w: True,
            pygame.K_s: False,
            pygame.K_a: False,
            pygame.K_d: False,
        }
        self.car.handle_movement(keys)
        assert self.car.vel > 0

    def test_handle_movement_rotation(self):
        keys = {
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_a: True,
            pygame.K_d: False,
        }
        self.car.handle_movement(keys)
        assert self.car.angle == 5

    def test_collide(self):
        self.car.x, self.car.y = 100, 150
        mock_mask = MagicMock()
        mock_mask.overlap.return_value = (5, 5)
        result = self.car.collide(mock_mask, x=90, y=140)
        assert result == (5, 5)
        mock_mask.overlap.assert_called_once()

if __name__ == "__main__":
    unittest.main()






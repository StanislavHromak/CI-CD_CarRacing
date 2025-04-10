import unittest
from unittest.mock import Mock, patch
from src.utils import scale_image, blit_rotate_center, blit_text_center


class TestUtils(unittest.TestCase):
    def test_scale_image(self):
        """
        Тестування масштабування зображення
        """
        mock_img = Mock()
        mock_img.get_width.return_value = 100
        mock_img.get_height.return_value = 200

        with patch('pygame.transform.scale') as mock_scale:
            mock_scaled_img = Mock()
            mock_scale.return_value = mock_scaled_img

            result = scale_image(mock_img, 2.0)

            mock_scale.assert_called_once_with(mock_img, (200, 400))
            self.assertEqual(result, mock_scaled_img)

    def test_blit_rotate_center(self):
        """
        Тестування обертання та відображення зображення
        """
        mock_win = Mock()
        mock_image = Mock()
        mock_image.get_rect.return_value = Mock(center=(50, 50))

        with patch('pygame.transform.rotate') as mock_rotate:
            mock_rotated = Mock()
            mock_rotated.get_rect.return_value = Mock(topleft=(30, 40))
            mock_rotate.return_value = mock_rotated

            blit_rotate_center(mock_win, mock_image, (10, 20), 90)

            mock_rotate.assert_called_once_with(mock_image, 90)
            mock_rotated.get_rect.assert_called_once_with(center=(50, 50))
            mock_win.blit.assert_called_once_with(mock_rotated, (30, 40))

    def test_blit_text_center(self):
        """
        Тестування відображення тексту в центрі
        """
        mock_win = Mock()
        mock_win.get_width.return_value = 800
        mock_win.get_height.return_value = 600
        mock_font = Mock()
        mock_render = Mock()
        mock_render.get_width.return_value = 100
        mock_render.get_height.return_value = 50
        mock_font.render.return_value = mock_render

        blit_text_center(mock_win, mock_font, "Test", (255, 255, 255))

        mock_font.render.assert_called_once_with("Test", 1, (255, 255, 255))
        mock_win.blit.assert_called_once_with(mock_render, (350, 275))


if __name__ == '__main__':
    unittest.main()
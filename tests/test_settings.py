import unittest
from src.settings import Settings


class TestSettings(unittest.TestCase):

    def setUp(self):
        """Ініціалізуємо об'єкт Settings перед кожним тестом."""
        self.settings = Settings()

    def test_initial_values(self):
        """Тестуємо початкові значення налаштувань."""
        self.assertEqual(self.settings.car_color, "red")
        self.assertEqual(self.settings.difficulty, "складний")
        self.assertEqual(self.settings.lives, 1)

    def test_set_car_color(self):
        """Тестуємо метод set_car_color."""
        self.settings.set_car_color("червоний")
        self.assertEqual(self.settings.car_color, "red")

        self.settings.set_car_color("білий")
        self.assertEqual(self.settings.car_color, "white")

        self.settings.set_car_color("фіолетовий")
        self.assertEqual(self.settings.car_color, "purple")

        self.settings.set_car_color("неіснуючий колір")
        self.assertEqual(self.settings.car_color, "red")

    def test_set_difficulty(self):
        """Тестуємо метод set_difficulty."""
        self.settings.set_difficulty("простий")
        self.assertEqual(self.settings.difficulty, "простий")
        self.assertEqual(self.settings.lives, 10)

        self.settings.set_difficulty("середній")
        self.assertEqual(self.settings.difficulty, "середній")
        self.assertEqual(self.settings.lives, 5)

        self.settings.set_difficulty("складний")
        self.assertEqual(self.settings.difficulty, "складний")
        self.assertEqual(self.settings.lives, 1)

    def test_reset_lives(self):
        """Тестуємо метод reset_lives."""
        self.settings.set_difficulty("простий")
        self.settings.reset_lives()
        self.assertEqual(self.settings.lives, 10)

        self.settings.set_difficulty("середній")
        self.settings.reset_lives()
        self.assertEqual(self.settings.lives, 5)

        self.settings.set_difficulty("складний")
        self.settings.reset_lives()
        self.assertEqual(self.settings.lives, 1)


if __name__ == "__main__":
    unittest.main()
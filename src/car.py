import pygame
import math
from src.utils import scale_image, blit_rotate_center

class Car:
    """
    Клас, що представляє машину гравця в грі 'CAR RACING'.
    Керує рухом, обертанням і зіткненнями машини на трасі.
    """
    START_POS = (180, 200) # Початкова позиція машини (x, y).

    def __init__(self, max_vel, rotation_vel, image_path):
        """
        Ініціалізує об’єкт машини з заданими параметрами.
        :param max_vel: Максимальна швидкість машини.
        :param rotation_vel: Швидкість обертання машини.
        :param image_path: Шлях до файлу зображення машини.
        """
        # Зображення машини, масштабоване до розміру гри.
        self.img = scale_image(pygame.image.load(image_path), 0.55)
        self.max_vel = max_vel # Максимальна швидкість машини.
        self.vel = 0 # Поточна швидкість машини.
        self.rotation_vel = rotation_vel # Швидкість обертання машини.
        self.angle = 0 # Кут повороту машини в градусах.
        self.x, self.y = self.START_POS # Поточні координати машини
        self.acceleration = 0.05 # Прискорення

    def rotate(self, left=False, right=False):
        """
        Обертає машину вліво або вправо.
        :param left: Якщо True, обертає машину вліво.
        :param right: Якщо True, обертає машину вправо.
        """
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        """
        Малює машину на екрані з урахуванням її позиції та кута повороту.
        :param win: Вікно Pygame для відображення машини.
        """
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        """
        Рухає машину вперед із прискоренням.
        Збільшує швидкість до максимальної межі та викликає рух.
        """
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        """
        Рухає машину назад із прискоренням.
        Зменшує швидкість до максимальної зворотної межі та викликає рух.
        """
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        """
        Оновлює позицію машини на основі її швидкості та кута.
        """
        radians = math.radians(self.angle)
        self.y -= math.cos(radians) * self.vel
        self.x -= math.sin(radians) * self.vel

    def reduce_speed(self):
        """
        Оновлює позицію машини на основі її швидкості та кута.
        Зменшує швидкість, якщо машина не рухається вперед або назад.
        """
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        """
        Перевіряє зіткнення машини з заданою маскою.
        :param mask: Маска об’єкта для перевірки зіткнення.
        :param x: Координата x об’єкта для порівняння (за замовчуванням 0).
        :param y: Координата у об’єкта для порівняння (за замовчуванням 0).
        :return: Координати точки зіткнення або None, якщо зіткнення немає.
        """
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        return mask.overlap(car_mask, offset)

    def reset(self, x=None, y=None):
        """
        Скидання позиції машини (на задані, якщо втрата життя, на старт, якщо початок рівня)
        :param x: Нова координата x.
        :param y: Нова координата у.
        """
        if x is None or y is None:
            self.x, self.y = self.START_POS
        else:
            self.x, self.y = x, y
        self.angle = 0
        self.vel = 0

    def handle_movement(self, keys):
        """
        Обробляє введення користувача для керування машиною.
        :param keys: W S A D (прямо, назад, вліво, вправо)
        """
        moved = False
        if keys[pygame.K_a]:
            self.rotate(left=True)
        if keys[pygame.K_d]:
            self.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            self.move_forward()
        if keys[pygame.K_s]:
            moved = True
            self.move_backward()
        if not moved:
            self.reduce_speed()
import pygame


def scale_image(img, factor):
    """
    Масштабує зображення за заданим коефіцієнтом.
    :param img: Зображення, яке потрібно масштабувати.
    :param factor: Коефіцієнт масштабування (наприклад, 2.0 для збільшення вдвічі).
    :return: Нове масштабоване зображення.
    """
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    """
    Обертає зображення із центром у заданій позиції.
    :param win: Вікно Pygame для відображення зображення.
    :param image: Зображення, яке потрібно повернути та відобразити.
    :param top_left: Координати верхнього лівого кута зображення перед обертанням.
    :param angle: Кут повороту в градусах (за годинниковою стрілкою для від’ємних значень).
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def blit_text_center(win, font, text, color):
    """
    Відображає текст у центрі вікна з заданим кольором.
    :param win: Вікно Pygame для відображення тексту.
    :param font: Шрифт для рендерингу тексту.
    :param text: Текст, який потрібно відобразити.
    :param color: Колір тексту у форматі RGB
    """
    render = font.render(text, 1, color)
    win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))
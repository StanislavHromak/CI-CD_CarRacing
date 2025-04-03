import time

class GameInfo:
    """
    Клас для відстеження стану гри та часу її виконання.
    """
    def __init__(self):
        self.started = False
        self.start_time = 0

    def start_game(self):
        """
        Розпочинає гру, встановлюючи початковий час.
        Встановлює прапорець started у True та фіксує поточний час як початок гри.
        """
        self.started = True
        self.start_time = time.time()

    def get_time(self):
        """
        Обчислює час, що минув з початку гри.
        :return: Кількість секунд, що минули з моменту виклику start_game. Повертає 0, якщо гра ще не розпочалася.
        """
        if self.started:
            elapsed = round(time.time() - self.start_time)
            return elapsed
        return 0
import time

class GameInfo:
    def __init__(self):
        self.started = False
        self.start_time = 0

    def start_game(self):
        self.started = True
        self.start_time = time.time()

    def get_time(self):
        return round(time.time() - self.start_time) if self.started else 0
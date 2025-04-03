import json

class Records:
    """
    Клас для збереження та керування рекордами гри 'CAR RACING'.
    """
    def __init__(self):
        self.best_times = {} # Словник, де ключ — номер рівня, значення — найкращий час проходження.
        self.record_level = 0 # Найвищий досягнутий рівень у грі.
        self.load_records()

    def load_records(self):
        """
        Завантажує рекорди з файлу 'records.json'
        Якщо файл не існує, ініціалізує порожні значення.
        Перетворює ключі best_times із рядків у цілі числа.
        """
        try:
            with open("../records.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.best_times = {int(k): v for k, v in data.get("best_times", {}).items()}
                self.record_level = data.get("level", 0)
        except FileNotFoundError:
            self.best_times = {}
            self.record_level = 0

    def save_records(self):
        """
        Зберігає поточні рекорди у файл 'records.json'.
        """
        data = {
            "best_times": self.best_times,
            "level": self.record_level
        }
        with open("../records.json", "w", encoding="utf-8") as f:
            json_string = json.dumps(data)
            f.write(json_string)

    def update_records(self, level, level_time):
        """
        Оновлює рекорди гри на основі нового рівня та часу проходження.
        :param level: Номер рівня, який було пройдено.
        :param level_time: Час проходження рівня в секундах.
        """
        if level not in self.best_times or level_time < self.best_times[level]:
            self.best_times[level] = level_time
            self.save_records()

        if level > self.record_level:
            self.record_level = level
            self.save_records()

    def get_record_info(self):
        """
        Повертає інформацію про рекорди для відображення.
        :return: Словник із найвищим рівнем і найкращими часами для рівнів 1–5,
        або None, якщо рекордів ще немає.
        """
        if self.record_level == 0:
            return None
        return {
            "level": self.record_level,
            "best_times": {i: self.best_times.get(i, 0) for i in range(1, 6)},
        }
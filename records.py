import json

class Records:
    def __init__(self):
        self.best_times = {}
        self.total_time_to_level = 0
        self.record_level = 0
        self.load_records()

    def load_records(self):
        try:
            with open("records.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.best_times = {int(k): v for k, v in data.get("best_times", {}).items()}
                self.record_level = data.get("level", 0)
        except FileNotFoundError:
            self.best_times = {}
            self.record_level = 0

    def save_records(self):
        data = {
            "best_times": self.best_times,
            "level": self.record_level
        }
        with open("records.json", "w", encoding="utf-8") as f:
            json_string = json.dumps(data)
            f.write(json_string)

    def update_records(self, level, level_time):
        if level not in self.best_times or level_time < self.best_times[level]:
            self.best_times[level] = level_time
            self.save_records()

        if level > self.record_level:
            self.record_level = level
            self.save_records()

    def get_record_info(self):
        if self.record_level == 0:
            return None
        return {
            "level": self.record_level,
            "best_times": {i: self.best_times.get(i, 0) for i in range(1, 6)},
        }
class Settings:
    def init(self):
        self.car_color = "red"
        self.difficulty = "складний"  # За замовчуванням
        self.lives = 1

    def set_car_color(self, color):
        color_mapping = {
            "червоний": "red",
            "білий": "white",
            "фіолетовий": "purple",
            "сірий": "grey",
            "зелений": "green"
        }
        self.car_color = color_mapping.get(color.lower(), "red")

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty.lower()
        if self.difficulty == "простий":
            self.lives = 10
        elif self.difficulty == "середній":
            self.lives = 5
        else:  # "складний"
            self.lives = 1

    def reset_lives(self):
        self.set_difficulty(self.difficulty)
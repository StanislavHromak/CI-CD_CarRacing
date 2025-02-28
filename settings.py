class Settings:
    """
    Клас для зберігання та керування налаштуваннями.
    """
    def __init__(self):
        """
        Ініціалізує об’єкт налаштувань із початковими значеннями.
        """
        self.car_color = "red"
        self.difficulty = "складний"
        self.lives = 1

    def set_car_color(self, color):
        """
        Встановлює колір машини на основі українського вводу.
        Перетворює українську назву кольору в англійську для використання в грі.
        :param color: Назва кольору українською
        :return:
        """
        color_mapping = {
            "червоний": "red",
            "білий": "white",
            "фіолетовий": "purple",
            "сірий": "grey",
            "зелений": "green"
        }
        self.car_color = color_mapping.get(color.lower(), "red")

    def set_difficulty(self, difficulty):
        """
        Встановлює рівень складності та відповідну кількість життів.
        :param difficulty: Рівень складності
        """
        self.difficulty = difficulty.lower()
        if self.difficulty == "простий":
            self.lives = 10
        elif self.difficulty == "середній":
            self.lives = 5
        else:
            self.lives = 1

    def reset_lives(self):
        """
        Скидає кількість життів до значень, що відповідають поточному рівню складності.
        """
        self.set_difficulty(self.difficulty)
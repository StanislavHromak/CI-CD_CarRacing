import unittest
from unittest.mock import patch, mock_open
import json
from src.records import Records


class TestRecords(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"best_times": {"1": 30, "2": 25}, "level": 2}')
    def test_load_records(self, mock_file):
        # Створюємо екземпляр класу Records
        records = Records()

        # Перевіряємо, що метод open був викликаний
        mock_file.assert_called_once_with("../records.json", "r", encoding="utf-8")

        # Перевіряємо, що рекорди були завантажені правильно
        self.assertEqual(records.best_times, {1: 30, 2: 25})
        self.assertEqual(records.record_level, 2)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_records(self, mock_file):
        # Створюємо екземпляр класу Records
        records = Records()

        # Встановлюємо нові рекорди
        records.best_times = {1: 15, 2: 20}
        records.record_level = 3

        # Викликаємо метод збереження
        records.save_records()

        # Перевіряємо, що файл був відкритий для читання і запису
        mock_file.assert_any_call("../records.json", "r", encoding="utf-8")
        mock_file.assert_any_call("../records.json", "w", encoding="utf-8")

        # Перевіряємо, що записані дані правильні (без відступів)
        expected_data = {
            "best_times": {1: 15, 2: 20},
            "level": 3
        }
        mock_file().write.assert_called_with(json.dumps(expected_data, ensure_ascii=False))

    @patch("builtins.open", new_callable=mock_open)
    def test_update_records(self, mock_file):
        # Створюємо екземпляр класу Records
        records = Records()

        # Оновлюємо рекорди
        records.update_records(3, 18)  # Рівень 3, час 18 секунд

        # Перевіряємо, чи були оновлені рекорди
        self.assertEqual(records.best_times[3], 18)
        self.assertEqual(records.record_level, 3)

        # Перевіряємо, чи був викликаний метод save_records
        mock_file.assert_called_with("../records.json", "w", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data='{"best_times": {"1": 10, "2": 15}, "level": 2}')
    def test_get_record_info(self, mock_file):
        # Створюємо екземпляр класу Records
        records = Records()

        # Перевіряємо, чи повертається правильна інформація
        record_info = records.get_record_info()
        expected_info = {
            "level": 2,
            "best_times": {1: 10, 2: 15, 3: 0, 4: 0, 5: 0}
        }
        self.assertEqual(record_info, expected_info)

    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    def test_get_record_info_when_no_records(self, mock_file):
        # Створюємо екземпляр класу Records
        records = Records()
        result = records.get_record_info()
        self.assertIsNone(result)  # Має бути None, оскільки рекордів немає


if __name__ == "main":
    unittest.main()
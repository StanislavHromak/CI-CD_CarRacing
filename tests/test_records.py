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
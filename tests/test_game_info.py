from unittest.mock import patch
from src.game_info import GameInfo

class TestGameInfo:
    @patch("src.game_info.time.time")
    def test_start_game_sets_started_and_time(self, mock_time):
        mock_time.return_value = 100.0  # Час старту

        game_info = GameInfo()
        game_info.start_game()

        assert game_info.started is True
        assert game_info.start_time == 100.0

    @patch("src.game_info.time.time")
    def test_get_time_when_started(self, mock_time):
        game_info = GameInfo()
        game_info.started = True
        game_info.start_time = 50.0

        mock_time.return_value = 52.3  # Поточний час = 52.3
        result = game_info.get_time()

        assert result == 3  # Округлено вгору з 2.3

    def test_get_time_when_not_started(self):
        game_info = GameInfo()
        result = game_info.get_time()
        assert result == 0
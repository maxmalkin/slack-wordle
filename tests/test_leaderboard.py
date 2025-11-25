import pytest
from datetime import date
from app.leaderboard import get_leaderboard_data, format_leaderboard_message

def test_get_leaderboard_data():
    data = get_leaderboard_data()
    assert "top_streaks" in data
    assert "top_win_rate" in data
    assert isinstance(data["top_streaks"], list)

def test_format_leaderboard_message():
    data = {
        "top_streaks": [("U123", "John", 10), ("U456", "Jane", 8)],
        "top_win_rate": [("U123", "John", 85.5), ("U789", "Bob", 80.0)]
    }
    message = format_leaderboard_message(data)
    assert "Leaderboard" in message
    assert "John" in message

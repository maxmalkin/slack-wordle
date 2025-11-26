import pytest
from datetime import date
from app.leaderboard import get_leaderboard_data, format_leaderboard_message, format_leaderboard_blocks

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

def test_format_leaderboard_blocks():
    data = {
        "top_streaks": [("U123", "John", 10), ("U456", "Jane", 8)],
        "top_win_rate": [("U123", "John", 85.5), ("U789", "Bob", 80.0)]
    }
    blocks = format_leaderboard_blocks(data)
    assert len(blocks) > 0
    assert any("Leaderboard" in str(block) for block in blocks)

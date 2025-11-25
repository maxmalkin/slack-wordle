import pytest
from app.blocks import build_game_board, build_stats_message, build_share_message
from datetime import date

def test_build_game_board():
    blocks = build_game_board(
        guesses=["cigar"],
        feedback=[["correct", "correct", "correct", "correct", "correct"]],
        attempts=1,
        status="won"
    )
    assert len(blocks) > 0
    assert any("Wordle" in str(block) for block in blocks)

def test_build_stats_message():
    blocks = build_stats_message(
        games_played=10,
        games_won=8,
        current_streak=3,
        max_streak=5,
        guess_distribution={"1": 0, "2": 1, "3": 3, "4": 2, "5": 2, "6": 0}
    )
    assert len(blocks) > 0

def test_build_share_message():
    message = build_share_message(
        game_date=date.today(),
        attempts=4,
        feedback=[
            ["absent", "present", "absent", "absent", "absent"],
            ["absent", "correct", "correct", "absent", "absent"],
            ["correct", "correct", "correct", "absent", "correct"],
            ["correct", "correct", "correct", "correct", "correct"]
        ]
    )
    assert "Wordle" in message
    assert "4/6" in message

import pytest
from datetime import date
from app.statistics import update_stats_after_game, get_user_stats, UserStats

def test_update_stats_after_win():
    update_stats_after_game("U12349", date.today(), won=True, attempts=3)
    stats = get_user_stats("U12349")
    assert stats.games_played == 1
    assert stats.games_won == 1
    assert stats.current_streak == 1
    assert stats.guess_distribution["3"] == 1

def test_update_stats_after_loss():
    update_stats_after_game("U12350", date.today(), won=False, attempts=6)
    stats = get_user_stats("U12350")
    assert stats.games_played == 1
    assert stats.games_won == 0
    assert stats.current_streak == 0

def test_get_user_stats_new_user():
    stats = get_user_stats("U12351")
    assert stats.games_played == 0
    assert stats.current_streak == 0

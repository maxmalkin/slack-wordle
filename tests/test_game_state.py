import pytest
from datetime import date
from app.game_state import get_or_create_game, submit_guess, GameState

def test_get_or_create_game_new():
    game = get_or_create_game("U12345", date.today())
    assert game.user_id == "U12345"
    assert game.status == "in_progress"
    assert game.attempts == 0
    assert game.guesses == []

def test_submit_guess_valid():
    game = get_or_create_game("U12346", date.today())
    result = submit_guess(game, "cigar")
    assert result.success == True
    assert len(result.feedback) == 5

def test_submit_guess_invalid():
    game = get_or_create_game("U12347", date.today())
    result = submit_guess(game, "zzzzz")
    assert result.success == False
    assert result.error == "Not in word list"

def test_submit_guess_wrong_length():
    game = get_or_create_game("U12348", date.today())
    result = submit_guess(game, "abc")
    assert result.success == False
    assert result.error == "Guess must be 5 letters"

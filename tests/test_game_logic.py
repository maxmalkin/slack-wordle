import pytest
from app.game_logic import evaluate_guess

def test_evaluate_guess_all_correct():
    result = evaluate_guess("cigar", "cigar")
    assert result == ["correct", "correct", "correct", "correct", "correct"]

def test_evaluate_guess_all_absent():
    result = evaluate_guess("abcde", "fghij")
    assert result == ["absent", "absent", "absent", "absent", "absent"]

def test_evaluate_guess_mixed():
    result = evaluate_guess("crane", "cigar")
    assert result == ["correct", "absent", "present", "absent", "absent"]

def test_evaluate_guess_duplicate_letters():
    result = evaluate_guess("speed", "erase")
    assert result == ["absent", "absent", "correct", "present", "absent"]

def test_evaluate_guess_duplicate_in_answer():
    result = evaluate_guess("robot", "floor")
    assert result == ["absent", "present", "absent", "present", "absent"]

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
    # c=correct, r=present (in pos 4), a=present (in pos 3), n=absent, e=absent
    assert result == ["correct", "present", "present", "absent", "absent"]

def test_evaluate_guess_duplicate_letters():
    result = evaluate_guess("speed", "erase")
    # s=present (in pos 3), p=absent, e=present (in pos 0 or 4), e=present (remaining e), d=absent
    assert result == ["present", "absent", "present", "present", "absent"]

def test_evaluate_guess_duplicate_in_answer():
    result = evaluate_guess("robot", "floor")
    # r=present (in pos 4), o=present (in pos 2 or 3), b=absent, o=correct (exact match), t=absent
    assert result == ["present", "present", "absent", "correct", "absent"]

import pytest
from app.word_list import load_answer_words, load_valid_words, is_valid_guess

def test_load_answer_words():
    words = load_answer_words()
    assert len(words) > 2000
    assert all(len(word) == 5 for word in words)
    assert all(word.islower() for word in words)

def test_load_valid_words():
    words = load_valid_words()
    assert len(words) > 10000
    assert all(len(word) == 5 for word in words)

def test_is_valid_guess():
    assert is_valid_guess("cigar") == True
    assert is_valid_guess("zzzzz") == False
    assert is_valid_guess("CIGAR") == True
    assert is_valid_guess("abc") == False

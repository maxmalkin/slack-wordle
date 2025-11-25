import pytest
from datetime import date, timedelta
from app.daily_word import get_daily_word, seed_daily_words

def test_seed_daily_words():
    seed_daily_words(days=30)
    word = get_daily_word(date.today())
    assert word is not None
    assert len(word) == 5

def test_get_daily_word_consistency():
    today = date.today()
    word1 = get_daily_word(today)
    word2 = get_daily_word(today)
    assert word1 == word2

def test_get_daily_word_different_days():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    seed_daily_words(days=30)
    word_today = get_daily_word(today)
    word_tomorrow = get_daily_word(tomorrow)
    assert word_today != word_tomorrow

from datetime import date, timedelta
from typing import Optional
import random
from app.database import execute_query, execute_query_one
from app.word_list import load_answer_words

def seed_daily_words(days: int = 365, start_date: Optional[date] = None):
    if start_date is None:
        start_date = date.today()

    answer_words = list(load_answer_words())
    random.seed(42)
    random.shuffle(answer_words)

    for i in range(days):
        current_date = start_date + timedelta(days=i)
        word = answer_words[i % len(answer_words)]

        try:
            execute_query(
                "INSERT INTO daily_words (date, word) VALUES (%s, %s) ON CONFLICT (date) DO NOTHING",
                (current_date, word)
            )
        except Exception:
            pass

def get_daily_word(target_date: date) -> Optional[str]:
    result = execute_query_one(
        "SELECT word FROM daily_words WHERE date = %s",
        (target_date,)
    )

    if result is None:
        seed_daily_words(days=7, start_date=target_date)
        result = execute_query_one(
            "SELECT word FROM daily_words WHERE date = %s",
            (target_date,)
        )

    return result[0] if result else None

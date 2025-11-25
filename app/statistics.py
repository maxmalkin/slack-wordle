from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict
import json
from app.database import execute_query, execute_query_one

@dataclass
class UserStats:
    user_id: str
    games_played: int
    games_won: int
    current_streak: int
    max_streak: int
    guess_distribution: Dict[str, int]
    last_played_date: date

def get_user_stats(user_id: str) -> UserStats:
    result = execute_query_one(
        "SELECT user_id, games_played, games_won, current_streak, max_streak, guess_distribution, last_played_date FROM user_stats WHERE user_id = %s",
        (user_id,)
    )

    if result:
        return UserStats(
            user_id=result[0],
            games_played=result[1],
            games_won=result[2],
            current_streak=result[3],
            max_streak=result[4],
            guess_distribution=result[5],
            last_played_date=result[6]
        )

    return UserStats(
        user_id=user_id,
        games_played=0,
        games_won=0,
        current_streak=0,
        max_streak=0,
        guess_distribution={"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0},
        last_played_date=None
    )

def update_stats_after_game(user_id: str, game_date: date, won: bool, attempts: int):
    stats = get_user_stats(user_id)

    games_played = stats.games_played + 1
    games_won = stats.games_won + (1 if won else 0)

    if won:
        if stats.last_played_date and stats.last_played_date == game_date - timedelta(days=1):
            current_streak = stats.current_streak + 1
        else:
            current_streak = 1
    else:
        current_streak = 0

    max_streak = max(stats.max_streak, current_streak)

    guess_distribution = stats.guess_distribution.copy()
    if won and 1 <= attempts <= 6:
        guess_distribution[str(attempts)] = guess_distribution.get(str(attempts), 0) + 1

    execute_query(
        """
        INSERT INTO user_stats (user_id, games_played, games_won, current_streak, max_streak, guess_distribution, last_played_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            games_played = EXCLUDED.games_played,
            games_won = EXCLUDED.games_won,
            current_streak = EXCLUDED.current_streak,
            max_streak = EXCLUDED.max_streak,
            guess_distribution = EXCLUDED.guess_distribution,
            last_played_date = EXCLUDED.last_played_date,
            updated_at = CURRENT_TIMESTAMP
        """,
        (user_id, games_played, games_won, current_streak, max_streak, json.dumps(guess_distribution), game_date)
    )

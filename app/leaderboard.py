from typing import List, Tuple, Dict
from app.database import execute_query

def get_leaderboard_data() -> Dict:
    top_streaks = execute_query(
        """
        SELECT user_id, current_streak
        FROM user_stats
        WHERE current_streak > 0
        ORDER BY current_streak DESC
        LIMIT 10
        """,
        fetch=True
    )

    top_win_rate = execute_query(
        """
        SELECT user_id,
               CASE WHEN games_played > 0
                    THEN (games_won::float / games_played * 100)
                    ELSE 0
               END as win_rate
        FROM user_stats
        WHERE games_played >= 5
        ORDER BY win_rate DESC
        LIMIT 10
        """,
        fetch=True
    )

    return {
        "top_streaks": [(row[0], None, row[1]) for row in (top_streaks or [])],
        "top_win_rate": [(row[0], None, row[1]) for row in (top_win_rate or [])]
    }

def format_leaderboard_message(data: Dict) -> str:
    message = "*Wordle Leaderboard*\n\n"

    message += "*Top Current Streaks:*\n"
    for i, (user_id, name, streak) in enumerate(data["top_streaks"][:10], 1):
        display_name = name or f"<@{user_id}>"
        message += f"{i}. {display_name}: {streak} days\n"

    message += "\n*Top Win Rates (min 5 games):*\n"
    for i, (user_id, name, win_rate) in enumerate(data["top_win_rate"][:10], 1):
        display_name = name or f"<@{user_id}>"
        message += f"{i}. {display_name}: {win_rate:.1f}%\n"

    return message

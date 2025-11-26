from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, timedelta
from app.daily_word import seed_daily_words
import logging
import os

logger = logging.getLogger(__name__)

def daily_word_check():
    logger.info("Running daily word check")
    tomorrow = date.today() + timedelta(days=1)
    seed_daily_words(days=7, start_date=tomorrow)
    logger.info("Daily word check complete")

def post_daily_summary():
    logger.info("Posting daily summary")
    try:
        from app import slack_app
        from app.database import execute_query

        channel_id = os.environ.get("WORDLE_CHANNEL_ID")
        if not channel_id:
            logger.warning("WORDLE_CHANNEL_ID not set, skipping daily summary")
            return

        active_streaks = execute_query(
            """
            SELECT user_id, current_streak
            FROM user_stats
            WHERE current_streak >= 2
            ORDER BY current_streak DESC
            LIMIT 10
            """,
            fetch=True
        )

        top_streaks = execute_query(
            """
            SELECT user_id, current_streak
            FROM user_stats
            WHERE current_streak > 0
            ORDER BY current_streak DESC
            LIMIT 5
            """,
            fetch=True
        )

        guess_dist = execute_query(
            """
            SELECT
                (guess_distribution->>'1')::int as g1,
                (guess_distribution->>'2')::int as g2,
                (guess_distribution->>'3')::int as g3,
                (guess_distribution->>'4')::int as g4,
                (guess_distribution->>'5')::int as g5,
                (guess_distribution->>'6')::int as g6
            FROM user_stats
            WHERE games_played > 0
            """,
            fetch=True
        )

        message = "*Daily Wordle Summary*\n\n"

        if active_streaks:
            message += "*Active Streaks (2+ days):*\n"
            for user_id, streak in active_streaks:
                message += f"<@{user_id}>: `{streak}` days\n"
            message += "\n"

        if top_streaks:
            message += "*Top Streaks:*\n"
            for i, (user_id, streak) in enumerate(top_streaks, 1):
                message += f"`#{i}` <@{user_id}>: *{streak}*\n"
            message += "\n"

        if guess_dist:
            total_dist = [0, 0, 0, 0, 0, 0]
            for row in guess_dist:
                for i in range(6):
                    total_dist[i] += row[i] if row[i] else 0

            total_games = sum(total_dist)
            if total_games > 0:
                message += "*Guess Distribution:*\n"
                for i in range(6):
                    count = total_dist[i]
                    pct = (count / total_games * 100) if total_games > 0 else 0
                    bar_len = int((count / max(total_dist)) * 15) if max(total_dist) > 0 else 0
                    bar = "▓" * bar_len
                    message += f"`{i+1}` {bar} `{count}` _{pct:.0f}%_\n"

        slack_app.client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        logger.info("Daily summary posted successfully")
    except Exception as e:
        logger.error(f"Error posting daily summary: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_word_check, 'cron', hour=0, minute=0)
    scheduler.add_job(post_daily_summary, 'cron', hour=9, minute=0)
    scheduler.start()
    logger.info("Scheduler started")

    seed_daily_words(days=365)
    logger.info("Initial word seeding complete")

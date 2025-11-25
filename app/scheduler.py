from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, timedelta
from app.daily_word import seed_daily_words
import logging

logger = logging.getLogger(__name__)

def daily_word_check():
    logger.info("Running daily word check")
    tomorrow = date.today() + timedelta(days=1)
    seed_daily_words(days=7, start_date=tomorrow)
    logger.info("Daily word check complete")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_word_check, 'cron', hour=0, minute=0)
    scheduler.start()
    logger.info("Scheduler started")

    seed_daily_words(days=365)
    logger.info("Initial word seeding complete")

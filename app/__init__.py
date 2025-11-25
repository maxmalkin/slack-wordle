from flask import Flask, request
import os
from dotenv import load_dotenv

load_dotenv()

flask_app = Flask(__name__)

# Only initialize Slack app if tokens are provided (not in test mode)
slack_app = None
handler = None

if os.environ.get("SLACK_BOT_TOKEN") and os.environ.get("SLACK_BOT_TOKEN") != "xoxb-your-bot-token-here":
    from slack_bolt import App
    from slack_bolt.adapter.flask import SlackRequestHandler

    slack_app = App(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
    )

    handler = SlackRequestHandler(slack_app)

    # Import handlers only when slack_app is initialized
    from app import slack_handlers

@flask_app.route("/slack/commands", methods=["POST"])
def slack_commands():
    return handler.handle(request)

@flask_app.route("/slack/interactions", methods=["POST"])
def slack_interactions():
    return handler.handle(request)

@flask_app.route("/health", methods=["GET"])
def health_check():
    from app.database import get_db_connection, close_db_connection
    try:
        conn = get_db_connection()
        close_db_connection(conn)
        return {"status": "ok", "database": "connected"}, 200
    except Exception as e:
        return {"status": "error", "database": str(e)}, 500

from app.scheduler import start_scheduler
start_scheduler()

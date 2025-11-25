from flask import Flask
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

from app import slack_handlers

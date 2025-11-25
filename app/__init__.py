from flask import Flask
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import os
from dotenv import load_dotenv

load_dotenv()

flask_app = Flask(__name__)

slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(slack_app)

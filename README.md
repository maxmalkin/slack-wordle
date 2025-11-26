# Slack Wordle

Daily Wordle game for Slack teams with statistics and leaderboards.

## Features

- Daily 5-letter word puzzle
- 6 attempts per game
- Color-coded feedback (green/yellow/gray)
- Personal statistics tracking
- Team leaderboards
- Current streak and max streak tracking
- Guess distribution charts
- Share results to channel

## Setup

1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure
4. Run database migrations: `psql $DATABASE_URL < migrations/init_db.sql`
5. Start app: `python run.py`

## Configuration

Set environment variables in `.env`:
- `SLACK_BOT_TOKEN`: Bot token from Slack app
- `SLACK_SIGNING_SECRET`: Signing secret from Slack app
- `DATABASE_URL`: PostgreSQL connection string
- `WORDLE_CHANNEL_ID`: Channel for leaderboards/summaries

## Commands

- `/wordle` - Play today's puzzle
- `/wordle stats` - View your statistics
- `/wordle leaderboard` - View team rankings

## Slack App Setup

1. Go to https://api.slack.com/apps
2. Click "Create New App" > "From an app manifest"
3. Select your workspace
4. Paste contents of `slack_manifest.json`
5. Install app to workspace
6. Copy Bot Token and Signing Secret to `.env`

## Deployment to Render

1. Push code to GitHub
2. Go to https://render.com
3. Click "New" > "Blueprint"
4. Connect your GitHub repository
5. Render will detect `render.yaml` and create services
6. Set environment variables in Render dashboard
7. Run database migration:
   - Open Shell in Render dashboard
   - Run: `psql $DATABASE_URL < migrations/init_db.sql`
8. Test with `/wordle` in Slack

## Development

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up database:
```bash
createdb wordle
psql wordle < migrations/init_db.sql
```

Run locally:
```bash
python run.py
```

Run tests:
```bash
pytest tests/ -v
```

## Architecture

- Flask web server with Slack Bolt SDK
- PostgreSQL database for persistence
- APScheduler for daily word rotation
- Block Kit for rich Slack UI
- Direct database access (no caching)

## License

MIT

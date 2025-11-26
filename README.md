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
- `/wordle reset` - Reset today's game and start over

## Architecture

- Flask web server with Slack Bolt SDK
- PostgreSQL database for persistence
- APScheduler for daily word rotation
- Block Kit for Slack UI

## License

MIT

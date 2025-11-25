# Slack Wordle

Daily Wordle game for Slack teams with statistics and leaderboards.

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
- `/wordle stats` - View personal statistics
- `/wordle leaderboard` - View team leaderboard

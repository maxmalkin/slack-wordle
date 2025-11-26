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

## Slack App Setup

1. Go to https://api.slack.com/apps
2. Click "Create New App" > "From an app manifest"
3. Select your workspace
4. Paste contents of `slack_manifest.yaml`
5. Replace `your-app.onrender.com` with your actual Render URL
6. Install app to workspace
7. Copy Bot Token and Signing Secret to `.env`

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
8. Update Slack app manifest with Render URL
9. Test with `/wordle` in Slack

## Commands

- `/wordle` - Play today's puzzle
- `/wordle stats` - View personal statistics
- `/wordle leaderboard` - View team leaderboard

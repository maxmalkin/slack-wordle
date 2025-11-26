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

CREATE TABLE IF NOT EXISTS daily_words (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    word VARCHAR(5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_games (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    guesses TEXT[] DEFAULT '{}',
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress',
    attempts INTEGER DEFAULT 0,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, date)
);

CREATE TABLE IF NOT EXISTS user_stats (
    user_id VARCHAR(255) PRIMARY KEY,
    games_played INTEGER DEFAULT 0,
    games_won INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    max_streak INTEGER DEFAULT 0,
    guess_distribution JSONB DEFAULT '{"1":0,"2":0,"3":0,"4":0,"5":0,"6":0}',
    last_played_date DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_games_user_date ON user_games(user_id, date);
CREATE INDEX IF NOT EXISTS idx_user_games_date ON user_games(date);
CREATE INDEX IF NOT EXISTS idx_daily_words_date ON daily_words(date);

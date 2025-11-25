from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from app.database import execute_query, execute_query_one
from app.daily_word import get_daily_word
from app.game_logic import evaluate_guess
from app.word_list import is_valid_guess

@dataclass
class GameState:
    id: int
    user_id: str
    date: date
    guesses: List[str]
    status: str
    attempts: int

@dataclass
class GuessResult:
    success: bool
    feedback: Optional[List[str]] = None
    error: Optional[str] = None
    game_won: bool = False
    game_lost: bool = False
    answer: Optional[str] = None

def get_or_create_game(user_id: str, game_date: date) -> GameState:
    result = execute_query_one(
        "SELECT id, user_id, date, guesses, status, attempts FROM user_games WHERE user_id = %s AND date = %s",
        (user_id, game_date)
    )

    if result:
        return GameState(
            id=result[0],
            user_id=result[1],
            date=result[2],
            guesses=result[3] if result[3] else [],
            status=result[4],
            attempts=result[5]
        )

    execute_query(
        "INSERT INTO user_games (user_id, date, status) VALUES (%s, %s, %s)",
        (user_id, game_date, "in_progress")
    )

    result = execute_query_one(
        "SELECT id, user_id, date, guesses, status, attempts FROM user_games WHERE user_id = %s AND date = %s",
        (user_id, game_date)
    )

    return GameState(
        id=result[0],
        user_id=result[1],
        date=result[2],
        guesses=result[3] if result[3] else [],
        status=result[4],
        attempts=result[5]
    )

def submit_guess(game: GameState, guess: str) -> GuessResult:
    if len(guess) != 5:
        return GuessResult(success=False, error="Guess must be 5 letters")

    if not is_valid_guess(guess):
        return GuessResult(success=False, error="Not in word list")

    answer = get_daily_word(game.date)
    feedback = evaluate_guess(guess, answer)

    new_guesses = game.guesses + [guess.lower()]
    new_attempts = game.attempts + 1

    game_won = all(f == "correct" for f in feedback)
    game_lost = new_attempts >= 6 and not game_won

    if game_won:
        new_status = "won"
    elif game_lost:
        new_status = "lost"
    else:
        new_status = "in_progress"

    execute_query(
        "UPDATE user_games SET guesses = %s, attempts = %s, status = %s WHERE id = %s",
        (new_guesses, new_attempts, new_status, game.id)
    )

    return GuessResult(
        success=True,
        feedback=feedback,
        game_won=game_won,
        game_lost=game_lost,
        answer=answer if (game_won or game_lost) else None
    )

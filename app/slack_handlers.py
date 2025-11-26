from datetime import date
from app import slack_app
from app.game_state import get_or_create_game, submit_guess
from app.statistics import get_user_stats, update_stats_after_game
from app.blocks import build_game_board, build_stats_message, build_share_message
from app.game_logic import evaluate_guess
from app.daily_word import get_daily_word

@slack_app.command("/wordle")
def handle_wordle_command(ack, command, say):
    ack()

    user_id = command["user_id"]
    text = command.get("text", "").strip()

    if text == "stats":
        stats = get_user_stats(user_id)
        blocks = build_stats_message(
            games_played=stats.games_played,
            games_won=stats.games_won,
            current_streak=stats.current_streak,
            max_streak=stats.max_streak,
            guess_distribution=stats.guess_distribution
        )
        say(blocks=blocks, text="Your Wordle Statistics")
        return

    if text == "leaderboard":
        from app.leaderboard import get_leaderboard_data, format_leaderboard_message
        data = get_leaderboard_data()
        message = format_leaderboard_message(data)
        say(text=message)
        return

    game = get_or_create_game(user_id, date.today())

    if game.status == "won":
        say(text=f"You already won today's puzzle in {game.attempts} attempts!")
        return

    if game.status == "lost":
        answer = get_daily_word(date.today())
        say(text=f"You already played today's puzzle. The answer was {answer.upper()}.")
        return

    feedback_list = []
    for guess in game.guesses:
        answer = get_daily_word(date.today())
        feedback = evaluate_guess(guess, answer)
        feedback_list.append(feedback)

    blocks = build_game_board(
        guesses=game.guesses,
        feedback=feedback_list,
        attempts=game.attempts,
        status=game.status
    )

    say(blocks=blocks, text="Wordle Game")

@slack_app.action("submit_guess")
def handle_submit_guess(ack, body, say):
    ack()

    user_id = body["user"]["id"]

    state_values = body["state"]["values"]
    guess_input_block = state_values.get("guess_input", {})
    guess_text_action = guess_input_block.get("guess_text", {})
    guess = guess_text_action.get("value", "").strip()

    game = get_or_create_game(user_id, date.today())
    result = submit_guess(game, guess)

    if not result.success:
        say(text=f"Error: {result.error}")
        return

    game = get_or_create_game(user_id, date.today())

    feedback_list = []
    for g in game.guesses:
        answer = get_daily_word(date.today())
        feedback = evaluate_guess(g, answer)
        feedback_list.append(feedback)

    blocks = build_game_board(
        guesses=game.guesses,
        feedback=feedback_list,
        attempts=game.attempts,
        status=game.status
    )

    if result.game_won or result.game_lost:
        update_stats_after_game(user_id, date.today(), result.game_won, game.attempts)

        if result.game_won:
            say(blocks=blocks, text=f"Congratulations! You won in {game.attempts} attempts!")
        else:
            say(blocks=blocks, text=f"Game over! The answer was {result.answer.upper()}.")
    else:
        say(blocks=blocks, text="Wordle Game")

from datetime import date
from app import slack_app
from app.game_state import get_or_create_game, submit_guess
from app.statistics import get_user_stats, update_stats_after_game
from app.blocks import build_game_board, build_stats_message, build_share_message
from app.game_logic import evaluate_guess
from app.daily_word import get_daily_word

@slack_app.command("/wordle")
def handle_wordle_command(ack, command, respond, client):
    ack()

    user_id = command["user_id"]
    channel_id = command["channel_id"]
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
        respond(blocks=blocks, text="Your Wordle Statistics", response_type="ephemeral")
        return

    if text == "leaderboard":
        from app.leaderboard import get_leaderboard_data, format_leaderboard_message
        data = get_leaderboard_data()
        message = format_leaderboard_message(data)
        respond(text=message, response_type="ephemeral")
        return

    game = get_or_create_game(user_id, date.today())

    answer = get_daily_word(date.today())

    if game.status == "won":
        respond(text=f"You already won today's puzzle in {game.attempts} attempts!", response_type="ephemeral")
        return

    if game.status == "lost":
        respond(text=f"You already played today's puzzle. The answer was {answer.upper()}.", response_type="ephemeral")
        return

    feedback_list = []
    for guess in game.guesses:
        feedback = evaluate_guess(guess, answer)
        feedback_list.append(feedback)

    blocks = build_game_board(
        guesses=game.guesses,
        feedback=feedback_list,
        attempts=game.attempts,
        status=game.status,
        answer=answer if game.status == "lost" else None
    )

    respond(blocks=blocks, text="Wordle Game", response_type="ephemeral")

@slack_app.action("submit_guess")
def handle_submit_guess(ack, body, respond):
    ack()

    user_id = body["user"]["id"]

    state_values = body["state"]["values"]
    guess_input_block = state_values.get("guess_input", {})
    guess_text_action = guess_input_block.get("guess_text", {})
    guess = guess_text_action.get("value", "").strip()

    game = get_or_create_game(user_id, date.today())
    result = submit_guess(game, guess)

    if not result.success:
        respond(text=f"Error: {result.error}", replace_original=False, response_type="ephemeral")
        return

    game = get_or_create_game(user_id, date.today())
    answer = get_daily_word(date.today())

    feedback_list = []
    for g in game.guesses:
        feedback = evaluate_guess(g, answer)
        feedback_list.append(feedback)

    blocks = build_game_board(
        guesses=game.guesses,
        feedback=feedback_list,
        attempts=game.attempts,
        status=game.status,
        answer=answer if game.status == "lost" else None
    )

    completion_text = "Wordle Game"
    if result.game_won or result.game_lost:
        update_stats_after_game(user_id, date.today(), result.game_won, game.attempts)

        if result.game_won:
            completion_text = f"Congratulations! You won in {game.attempts} attempts!"
        else:
            completion_text = f"Game over! The answer was {result.answer.upper()}."

    respond(
        blocks=blocks,
        text=completion_text,
        replace_original=True,
        response_type="ephemeral"
    )

from typing import List, Dict
from datetime import date

def build_game_board(guesses: List[str], feedback: List[List[str]], attempts: int, status: str) -> List[Dict]:
    blocks = []

    header_text = f"Wordle - Attempt {attempts}/6"
    if status == "won":
        header_text = f"Wordle - Solved in {attempts}!"
    elif status == "lost":
        header_text = "Wordle - Better luck tomorrow!"

    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": header_text
        }
    })

    board_text = ""
    for i, guess in enumerate(guesses):
        guess_feedback = feedback[i]
        squares = "".join(
            "🟩" if f == "correct" else "🟨" if f == "present" else "⬛"
            for f in guess_feedback
        )
        board_text += f"{squares} {guess.upper()}\n"

    for _ in range(6 - len(guesses)):
        board_text += "⬜⬜⬜⬜⬜\n"

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": board_text
        }
    })

    if status == "in_progress":
        blocks.append({
            "type": "input",
            "block_id": "guess_input",
            "element": {
                "type": "plain_text_input",
                "action_id": "guess_text",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Enter your 5-letter guess"
                }
            },
            "label": {
                "type": "plain_text",
                "text": "Your Guess"
            }
        })

        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Submit Guess"
                    },
                    "action_id": "submit_guess",
                    "style": "primary"
                }
            ]
        })

    return blocks

def build_stats_message(games_played: int, games_won: int, current_streak: int, max_streak: int, guess_distribution: Dict[str, int]) -> List[Dict]:
    win_percentage = (games_won / games_played * 100) if games_played > 0 else 0

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Your Wordle Statistics"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Games Played:*\n{games_played}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Win %:*\n{win_percentage:.0f}%"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Current Streak:*\n{current_streak}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Max Streak:*\n{max_streak}"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Guess Distribution:*"
            }
        }
    ]

    max_count = max(guess_distribution.values()) if guess_distribution.values() else 1
    for i in range(1, 7):
        count = guess_distribution.get(str(i), 0)
        bar_length = int((count / max_count) * 20) if max_count > 0 else 0
        bar = "█" * bar_length
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{i}: {bar} {count}"
            }
        })

    return blocks

def build_share_message(game_date: date, attempts: int, feedback: List[List[str]]) -> str:
    date_str = game_date.strftime("%Y-%m-%d")
    message = f"Wordle {date_str} {attempts}/6\n\n"

    for guess_feedback in feedback:
        squares = "".join(
            "🟩" if f == "correct" else "🟨" if f == "present" else "⬛"
            for f in guess_feedback
        )
        message += squares + "\n"

    return message

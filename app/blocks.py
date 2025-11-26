from typing import List, Dict
from datetime import date

def calculate_letter_states(guesses: List[str], feedback: List[List[str]]) -> Dict[str, str]:
    letter_states = {}

    for i, guess in enumerate(guesses):
        for j, letter in enumerate(guess.lower()):
            current_state = feedback[i][j]
            existing_state = letter_states.get(letter, "unused")

            if current_state == "correct":
                letter_states[letter] = "correct"
            elif current_state == "present" and existing_state != "correct":
                letter_states[letter] = "present"
            elif letter not in letter_states:
                letter_states[letter] = "absent"

    return letter_states

def build_keyboard(letter_states: Dict[str, str]) -> str:
    keyboard_rows = [
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
    ]

    keyboard_text = "\n"
    for row in keyboard_rows:
        row_text = ""
        for letter in row:
            state = letter_states.get(letter.lower(), "unused")
            if state == "correct":
                row_text += f"🟩*{letter}* "
            elif state == "present":
                row_text += f"🟨*{letter}* "
            elif state == "absent":
                row_text += f"⬛*{letter}* "
            else:
                row_text += f"⬜*{letter}* "
        keyboard_text += row_text.strip() + "\n"

    return keyboard_text

def build_game_board(guesses: List[str], feedback: List[List[str]], attempts: int, status: str, answer: str = None) -> List[Dict]:
    blocks = []

    header_text = f"Wordle - Attempt {attempts}/6"
    if status == "won":
        header_text = f"Wordle - Solved in {attempts}!"
    elif status == "lost":
        header_text = f"Wordle - Better luck tomorrow! The answer was: {answer.upper()}"

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

    letter_states = calculate_letter_states(guesses, feedback)
    keyboard = build_keyboard(letter_states)
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": keyboard
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
    games_lost = games_played - games_won

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Your Wordle Statistics"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*OVERALL PERFORMANCE*\n\n*Total Games:* `{games_played}`\n*Wins:* `{games_won}` | *Losses:* `{games_lost}`\n*Win Rate:* *`{win_percentage:.1f}%`*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*CURRENT STREAK*\n`{current_streak}` days"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*MAX STREAK*\n`{max_streak}` days"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*GUESS DISTRIBUTION*"
            }
        }
    ]

    max_count = max(guess_distribution.values()) if guess_distribution.values() else 1
    for i in range(1, 7):
        count = guess_distribution.get(str(i), 0)
        bar_length = int((count / max_count) * 25) if max_count > 0 else 0
        bar = "▓" * bar_length
        percentage = (count / games_played * 100) if games_played > 0 else 0

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"`{i}` {bar} *{count}* _{percentage:.0f}%_"
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

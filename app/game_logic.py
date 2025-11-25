from typing import List

def evaluate_guess(guess: str, answer: str) -> List[str]:
    guess = guess.lower()
    answer = answer.lower()
    result = ["absent"] * 5
    answer_chars = list(answer)

    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = "correct"
            answer_chars[i] = None

    for i in range(5):
        if result[i] == "absent" and guess[i] in answer_chars:
            result[i] = "present"
            answer_chars[answer_chars.index(guess[i])] = None

    return result

def format_feedback_squares(feedback: List[str]) -> str:
    mapping = {
        "correct": "🟩",
        "present": "🟨",
        "absent": "⬛"
    }
    return "".join(mapping[status] for status in feedback)

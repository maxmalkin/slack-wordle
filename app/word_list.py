import os
from typing import Set

_answer_words: Set[str] = set()
_valid_words: Set[str] = set()

def load_answer_words() -> Set[str]:
    global _answer_words
    if not _answer_words:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'wordle_answers.txt')
        with open(file_path, 'r') as f:
            _answer_words = set(word.strip().lower() for word in f.readlines())
    return _answer_words

def load_valid_words() -> Set[str]:
    global _valid_words
    if not _valid_words:
        answer_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'wordle_answers.txt')
        guess_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'wordle_guesses.txt')

        with open(answer_path, 'r') as f:
            words = set(word.strip().lower() for word in f.readlines())

        with open(guess_path, 'r') as f:
            words.update(word.strip().lower() for word in f.readlines())

        _valid_words = words
    return _valid_words

def is_valid_guess(guess: str) -> bool:
    if len(guess) != 5:
        return False
    valid_words = load_valid_words()
    return guess.lower() in valid_words

from .consts import Letter, Accidental

def nth_letter_from(letter: Letter, nth: int) -> Letter:
    letters = list(Letter)
    return letters[(letters.index(letter) + nth) % 7]

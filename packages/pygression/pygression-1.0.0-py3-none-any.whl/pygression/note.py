from .utils import nth_letter_from
from .consts import Letter, Accidental, AS_NOTATION

class Note:
    """
    A class representing a musical note.

    Args:
        letter (Letter): The letter of the note.
        accidental (Accidental, optional): The accidental of the note. Defaults to natural.
    """

    def __init__(self, letter: Letter, accidental: Accidental = Accidental.NATURAL):
        self._letter = letter
        self._accidental = accidental

    def __int__(self) -> int:
        return (self._letter.value + self._accidental.value) % 12

    def __repr__(self) -> str:
        return AS_NOTATION[self._letter] + AS_NOTATION[self._accidental]

    def __str__(self) -> str:
        return AS_NOTATION[self._letter] + AS_NOTATION[self._accidental]

    def __iadd__(self, semitones: int) -> "Note":
        """
        Transpose the note up by modifying its accidental in-place.

        Args:
            semitones (int): The number of semitones to transpose up by.

        Returns:
            Note: The transposed note.
        """

        self._accidental = Accidental(self._accidental.value + semitones)
        return self

    def __add__(self, semitones: int) -> "Note":
        """
        Return a new note transposed up by a number of semitones.

        Args:
            semitones (int): The number of semitones to transpose up by.

        Returns:
            Note: The transposed note.
        """

        return Note(self._letter, Accidental(self._accidental.value + semitones))

    def __isub__(self, semitones: int) -> "Note":
        """
        Transpose the note down by modifying its accidental in-place.

        Args:
            semitones (int): The number of semitones to transpose down by.

        Returns:
            Note: The transposed note.
        """

        return self.__iadd__(-semitones)

    def __sub__(self, semitones: int) -> "Note":
        """
        Return a new note transposed down by a number of semitones.

        Args:
            semitones (int): The number of semitones to transpose down by.

        Returns:
            Note: The transposed note.
        """

        return self.__add__(-semitones)

    def __rshift__(self, shift: int) -> "Note":
        """
        Return a new note with its letter shifted up.

        Args:
            shift (int): The number of letters to shift right by.

        Returns:
            Note: The transposed note.
        """
        
        return Note(nth_letter_from(self._letter, shift), self._accidental)

    def __irshift__(self, shift: int) -> "Note":
        """
        Transpose the note up by shifting its letter in-place.

        Args:
            shift (int): The number of letters to shift right by.

        Returns:
            Note: The transposed note.
        """

        self._letter = nth_letter_from(self._letter, shift)
        return self

    def __lshift__(self, shift: int) -> "Note":
        """
        Return a new note with its letter shifted down.

        Args:
            shift (int): The number of letters to shift left by.

        Returns:
            Note: The transposed note.
        """

        return self.__rshift__(-shift)

    def __ilshift__(self, shift: int) -> "Note":
        """
        Transpose the note down by shifting its letter in-place.

        Args:
            shift (int): The number of letters to shift left by.

        Returns:
            Note: The transposed note.
        """

        return self.__irshift__(-shift)

    def __eq__(self, other: "Note") -> bool:
        """
        Check for enharmonic equivalence with another note.

        Args:
            other (Note): The note to compare with.

        Returns:
            bool: True if the notes are enharmonically equivalent, False otherwise.
        """

        return int(self) == int(other)

    def __ne__(self, other: "Note") -> bool:
        """
        Check for enharmonic inequivalence with another note.

        Args:
            other (Note): The note to compare with.

        Returns:
            bool: True if the notes are enharmonically different, False otherwise.
        """

        return int(self) != int(other)

    @property
    def letter(self) -> Letter:
        """
        Get the letter of the note.

        Returns:
            Letter: The note's letter.
        """

        return self._letter

    @letter.setter
    def letter(self, new_letter: Letter):
        """
        Set the letter of the note.

        Args:
            new_letter (Letter): The new letter to set.
        """

        self._letter = new_letter

    @property
    def accidental(self) -> Accidental:
        """
        Get the accidental of the note.

        Returns:
            Accidental: The note's accidental.
        """

        return self._accidental

    @accidental.setter
    def accidental(self, new_accidental: Accidental):
        """
        Set the accidental of the note.

        Args:
            new_accidental (Accidental): The new accidental to set.
        """

        self._accidental = new_accidental

    @staticmethod
    def note_relative_to(letter: Letter, root: "Note", semitones: int) -> "Note":
        """
        Get a note a specified number of semitones away from a root note with a given letter.

        Args:
            letter (Letter): The desired letter of the resulting note.
            root (Note): The root note to base the transposition on.
            semitones (int): The number of semitones away from the root.

        Returns:
            Note: The resulting transposed note.

        Raises:
            ValueError: If the resulting note cannot be expressed with the given letter.
        """
        
        accidental = (semitones - (letter.value - int(root) + root.accidental.value) % 12)
        if accidental > 2:
            accidental -= 12

        return Note(letter, Accidental(accidental + root.accidental.value))

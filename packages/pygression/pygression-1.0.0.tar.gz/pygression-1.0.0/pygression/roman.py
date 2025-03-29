from .consts import Accidental, AS_NOTATION, ROMAN

class Roman:
    """
    Class that represents a Roman numeral with accidentals (nonexistent in music theory).

    Args:
        degree (int): Degree of the numeral.
        accidental (Accidental): Accidental of the numeral. If left blank, the note defaults to natural.
    """

    def __init__(self, degree: int, accidental: Accidental=Accidental.NATURAL):
        self._degree = degree
        self._accidental = accidental

    def __int__(self) -> int:
        return (self._degree + self._accidental.value) % 12

    def __repr__(self) -> str:
        return AS_NOTATION[self._accidental] + ROMAN[self._degree - 1]

    def __str__(self) -> str:
        return AS_NOTATION[self._accidental] + ROMAN[self._degree - 1]
    
    # Accidental change
    def __iadd__(self, semitones: int) -> "Roman":
        """
        Transposes the numeral up by changing the accidental.

        Args:
            semitones (int): Amount of semitones to move up by.
        
        Returns:
            Roman: The transposed numeral.
        """

        self._accidental = Accidental(self._accidental.value + semitones)

        return self
    
    def __add__(self, semitones: int) -> "Roman":
        """
        Returns a new numeral resulting from transposing a numeral up by changing the accidental.

        Args:
            semitones (int): Amount of semitones to move up by.
        
        Returns:
            Roman: The transposed numeral.
        """

        return Roman(self._degree, Accidental(self._accidental.value + semitones))

    def __isub__(self, semitones: int) -> "Roman":
        """
        Transposes the numeral down by changing the accidental.

        Args:
            semitones (int): Amount of semitones to move up by.
        
        Returns:
            Roman: The transposed numeral.
        """

        return self.__iadd__(-semitones)
    
    def __sub__(self, semitones: int) -> "Roman":
        """
        Returns a new numeral resulting from transposing a numeral down by changing the accidental.

        Args:
            semitones (int): Amount of semitones to move down by.
        
        Returns:
            Roman: The transposed numeral.
        """

        return self.__add__(-semitones)
    
    def __rshift__(self, shift: int) -> "Roman":
        """
        Returns a new numeral resulting from transposing a numeral up by shifting the degree.

        Args:
            shift (int): Amount of degrees to shift right by.
        
        Returns:
            Roman: The transposed numeral.
        """

        return Roman((self._degree + shift) % 7 + 1, self._accidental)
    
    def __irshift__(self, shift: int) -> "Roman":
        """
        Transposes the numeral up by shifting the degree of the note to the right a specified amount of times.

        Args:
            shift (int): Amount of degrees to shift right by.
        
        Returns:
            Roman: The transposed numeral.
        """

        self._degree = (self._degree + shift) % 7 + 1
        return self
    
    def __lshift__(self, shift: int) -> "Roman":
        """
        Returns a new numeral resulting from transposing a numeral down by shifting the degree.

        Args:
            shift (int): Amount of degrees to shift left by.
        
        Returns:
            Roman: The transposed numeral.
        """

        return self.__rshift__(-shift)

    def __ilshift__(self, shift: int) -> "Roman":
        """
        Transposes the numeral down by shifting the degree of the numeral to the left a specified amount of times.

        Args:
            shift (int): Amount of degrees to shift left by.
        
        Returns:
            Roman: The transposed numeral.
        """

        return self.__irshift__(-shift)

    def __eq__(self, other: "Roman") -> bool:
        """
        Checks for enharmonic equivalence.

        Args:
            other (Roman): Numeral to compare the current numeral to.
        
        Returns:
            bool: Whether the two numerals are enharmonically equivalent.
        """

        return int(self) == int(other)
    
    def __ne__(self, other: "Roman") -> bool:
        """
        Checks for enharmonic inequivalence.

        Args:
            other (Roman): Numeral to compare the current numeral to.
        
        Returns:
            bool: Whether the two numerals are enharmonically inequivalent.
        """

        return int(self) != int(other)
    
    @property
    def degree(self) -> int:
        """
        Get the degree of the numeral.

        Returns: 
            int: Degree of the numeral.
        """

        return self._degree

    @degree.setter
    def degree(self, new_degree: int):
        """
        Set the degree of the numeral.

        Args:
            new_degree (int): Integer to set to.
        """
        
        self._letter = new_degree
    
    @property
    def accidental(self) -> Accidental:
        """
        Get the accidental of the note.

        Returns: 
            Accidental: Accidental of the note.
        """

        return self._accidental

    @accidental.setter
    def accidental(self, new_accidental: Accidental):
        """
        Set the accidental of the note.

        Args:
            new_accidental (Accidental): Accidental to set to.
        """
        
        self._accidental = new_accidental
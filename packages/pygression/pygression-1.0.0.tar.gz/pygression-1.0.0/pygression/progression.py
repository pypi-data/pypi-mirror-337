# Basically a list specifically tailored to chord progressions
from typing import List
from copy import deepcopy
from .chord import Chord
from .roman import Roman
from .romanchord import RomanChord
from .note import Note
from .consts import Accidental, Mode
from .quality.triad import *

class Progression:
    """
    Class that represents chord progressions.

    Args:
        items (List): List of chords represented as either Roman chords or degrees.
        mode (Mode): Mode that the degrees are based off of.
        relative_to (Mode): Mode that the progression is read with respect to.
    """

    def __init__(self, items=None, mode: Mode=Mode.ION, relative_to: Mode=Mode.ION):
        self._mode = mode
        self._relative_to = relative_to
        self._chords = []

        for item in items:
            self.append(item)

    def _calculate_scale(self, mode: Mode) -> List[Note]:
        scale = []
        for i in range(7):
            scale.append(self._key >> i)

        for i in range(7):
            semitones = (mode.value[i] + int(self._key) - int(scale[i])) % 12
            if semitones > 2:
                semitones -= 12
                
            scale[i] += semitones
        
        return scale
    
    def __repr__(self) -> str:
        return str(self._chords)

    def __str__(self) -> str:
        return str(self._chords)

    def __add__(self, prog: "Progression") -> "Progression":
        """
        Returns a progression with chords from one progression added to the end of the current progression.

        Args:
            prog (Progression): Progression to add chords from.
        
        Returns:
            Progression: A new progression with chords appended to it.
        """

        new_prog = deepcopy(self)
        new_prog._chords += prog._chords

        return new_prog
    
    def __iadd__(self, prog: "Progression") -> "Progression":
        """
        Adds chords from one progression to the end of the current progression.

        Args:
            prog (Progression): Progression to add chords from.
        
        Returns:
            Progression: The progression with chords appended to it.
        """

        if type(prog) != Progression:
            raise TypeError(f"prog must be Progression, not {type(prog).__name__}")

        self._chords += prog._chords
        return self

    def __getitem__(self, index: int) -> RomanChord:
        """
        Get Roman chord in the progression at a specific index.

        Args:
            index (int): Index of Roman chord in progression.
        
        Returns:
            RomanChord: The Roman chord at the index.

        Raises:
            IndexError: If "index" is not in the range of the list of notes.
        """

        return self._chords[index]
    
    def __setitem__(self, index: int, new_item):
        """
        Set Roman chord in the progression at a specific index.

        Args:
            index (int): Index of Roman chord in progression.
            new_item (int, RomanChord): Roman chord to set to.

        Raises:
            IndexError: If "index" is not in the range of the list of notes.
            ValueError: If "new_item" is a degree and is not between 1 and 7.
        """

        new_chord = None

        if type(new_item) == int:
            self._append_degree(new_item)
            new_chord = self._chords.pop()
        elif type(new_item) == RomanChord:
            new_chord = new_item

        self._chords[index] = new_chord
    
    @property
    def mode(self) -> Mode:
        """
        Get mode of progresion.

        Returns:
            Mode: Mode of the progression.
        """

        return self._mode
    
    # Mode change
    @mode.setter
    def mode(self, new_mode: Mode):
        """
        Set mode of progression.

        Args:
            new_mode (Mode): Mode to set the progression to.
        """

        self._mode = new_mode
    
    @property
    def relative_to(self) -> Mode:
        """
        Get mode that progresion is read with respect to.

        Returns:
            Mode: Mode the progression is read with respect to.
        """

        return self._relative_to
    
    @relative_to.setter
    def relative_to(self, new_mode: Mode):
        """
        Set mode that progression is read with respect to.

        Args:
            new_mode (Mode): Mode to set the progression to.
        """

        for chord in self._chords:
            chord.roman += new_mode - self._relative_to

            if chord._target != None:
                chord._target.roman += new_mode - self._relative_to

        self._relative_to = new_mode
    
    @property
    def chords(self) -> List[RomanChord]:
        """
        Get list of Roman chords in progression.

        Returns:
            List[RomanChord]: Roman chords in progression.
        """

        return self._chords
    
    def _append_degree(self, degree: int):
        if degree < 1 or degree > 7:
            raise ValueError("degree must be between 1 and 7")

        scale = self._mode.value
        integers = [int(scale[degree - 1]), int(scale[(degree + 1) % 7]), int(scale[(degree + 3) % 7])]
        integers[1] -= integers[0]
        integers[1] %= 12
        integers[2] -= integers[0]
        integers[2] %= 12
        integers[0] = 0

        quality = None

        if integers == Major._get_integers():
            quality = Major()
        elif integers == Minor._get_integers():
            quality = Minor()
        elif integers == Diminished._get_integers():
            quality = Diminished()
        elif integers == Augmented._get_integers():
            quality = Augmented()

        self._chords.append(RomanChord(Roman(degree, accidental=Accidental(self._mode.value[degree - 1] - self._relative_to.value[degree - 1])), quality=quality))

    def _append_chord(self, chord: Chord):
        self._chords.append(chord)
    
    def _insert_degree(self, degree: int, index: int):
        if degree < 1 or degree > 7:
            raise ValueError("degree must be between 1 and 7")

        scale = self._mode.value
        integers = [int(scale[degree - 1]), int(scale[(degree + 1) % 7]), int(scale[(degree + 3) % 7])]
        integers[1] -= integers[0]
        integers[1] %= 12
        integers[2] -= integers[0]
        integers[2] %= 12
        integers[0] = 0

        quality = None

        if integers == Major._get_integers():
            quality = Major()
        elif integers == Minor._get_integers():
            quality = Minor()
        elif integers == Diminished._get_integers():
            quality = Diminished()
        elif integers == Augmented._get_integers():
            quality = Augmented()
        
        self._chords.insert(index, RomanChord(Roman(degree, accidental=Accidental(self._mode.value[degree - 1] - self._relative_to.value[degree - 1])), quality=quality))
    
    def _insert_chord(self, chord: RomanChord, index: int):
        self._chords.insert(index, chord)

    def append(self, item):
        """
        Appends a Roman chord to the progression.

        Args:
            item (int, RomanChord): Roman chord to append to the progression.
        
        Raises:
            ValueError: If "new_item" is a degree and is not between 1 and 7.
        """

        if type(item) == int:
            self._append_degree(item)
        elif type(item) == RomanChord:
            self._append_chord(item)
        else:
            raise TypeError(f"item must be integer or RomanChord, not {type(item).__name__}")
    
    def insert(self, index: int, item):
        """
        Inserts a Roman chord into the progression.

        Args:
            index (int): Index to insert at.
            item (int, RomanChord): Roman chord to append to the progression.
        
        Raises:
            IndexError: If "index" is not in the range of the list of Roman chords.
            ValueError: If "new_item" is a degree and is not between 1 and 7.
        """

        if type(item) == int:
            self._insert_degree(item, index)
        elif type(item) == RomanChord:
            self._insert_chord(item, index)
    
    def pop(self, index: int=-1) -> RomanChord:
        """
        Removes and returns the Roman chord in the progression at the specified index.

        Args:
            index (int): Index to pop the Roman chord from.

        Returns:
            RomanChord: Roman chord at the index.
        """

        return self._chords.pop(index)
    
    def chords_in(self, key: Note) -> List[Chord]:
        """
        Get the chords of the chord progression in a specific key.

        Args:
            key (Note): Key of chord progression.

        Returns:
            List[Chord]: List of chords in a specific key.

        Raises:
            ValueError: If "key" has double accidentals.
        """

        if key.accidental.value < -1 or key.accidental.value > 1:
            raise ValueError("cannot have double accidentals as key")

        chords = []
        scale = self._relative_to.value

        for chord in self._chords:
            degree = (chord.roman.degree + (0 if chord._target == None else chord._target.roman.degree - 1)) % 7

            root = Note(key.letter) >> (degree - 1)
            accidental = scale[degree - 1] + chord.roman.accidental.value + (chord._target.roman.accidental.value if chord._target != None else 0) - (int(root) - int(key))
            if accidental > 2:
                accidental -= 12
            root.accidental = Accidental(accidental)
            
            new_chord = Chord(root, quality=chord.quality) >> chord._inversion
            new_chord.modifiers = deepcopy(chord._modifiers)

            chords.append(new_chord)

        return chords
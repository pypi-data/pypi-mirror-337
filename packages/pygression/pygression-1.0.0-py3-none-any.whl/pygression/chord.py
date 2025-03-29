from typing import List
from copy import deepcopy
from .note import Note
from .utils import nth_letter_from
from .quality.base import Quality
from .quality.triad import Major, Minor
from .modifier.base import Modifier

class Chord:
    """
    Class that represents a chord in music.

    Args:
        root (Note): Root of the chord.
        quality (Quality): Quality of the chord.
    """

    def __init__(self, root: Note, quality: Quality=Major()):
        self._root = root
        self._quality = quality
        self._inversion = 0
        self._modifiers = []
        self._notes = []

        self._calculate_notes()
    
    def __repr__(self) -> str:
        return str(self._root) + str(self._quality) + self._quality._figured_bass(0) + "".join(str(modifier) for modifier in self._modifiers) + ("/" + str(self._notes[0]) if self._inversion != 0 else "")

    def __str__(self) -> str:
        return str(self._root) + str(self._quality) + self._quality._figured_bass(0) + "".join(str(modifier) for modifier in self._modifiers) + ("/" + str(self._notes[0]) if self._inversion != 0 else "")
    
    def attach(self, new_modifier: Modifier) -> "Chord":
        """
        Adds a modifier to the chord.

        Args:
            new_modifier: Modifier to add to the chord.

        Returns: 
            Chord: The chord with the modifier added.
        """

        if new_modifier not in self._modifiers:
            self._modifiers.append(new_modifier)
        self._modifiers = sorted([modifier for modifier in self._modifiers if new_modifier._compatible_with_mod(modifier)])
        self._calculate_notes()

        return self

    def detach(self, modifier: Modifier) -> "Chord":
        """
        Removes a modifier from the chord.

        Args:
            modifier: Modifier to remove from the chord.

        Returns:
            Chord: The chord with the modifier removed.
        """

        self._modifiers.remove(modifier)
        return self

    def with_mod(self, new_modifier: Modifier) -> "Chord":
        """
        Returns a chord with the supplied modifier.

        Args:
            new_modifier: Modifier to add to the chord.

        Returns: 
            Chord: A new chord with the modifier added.
        """
        
        new_chord = deepcopy(self)
        if new_modifier not in new_chord._modifiers:
            new_chord._modifiers.append(new_modifier)
        new_chord._modifiers = sorted([modifier for modifier in new_chord._modifiers if new_modifier._compatible_with_mod(modifier)])
        new_chord._calculate_notes()

        return new_chord            

    def without_mod(self, modifier: Modifier) -> "Chord":
        """
        Returns a chord without the supplied modifier.

        Args:
            modifier: Modifier to remove from the chord.

        Returns: 
            Chord: The chord with the modifier removed.
        """

        new_chord = deepcopy(self)
        new_chord._modifiers.remove(modifier)

        return new_chord

    def __irshift__(self, inversions: int) -> "Chord":
        """
        Inverts a chord up by a certain amount of inversions

        Args:
            inversions (int): Number of times to invert up.
        
        Returns: 
            Chord: The chord inverted.
        """

        self._inversion += inversions
        self._calculate_notes()
        
        return self

    def __rshift__(self, inversions: int) -> "Chord":
        """
        Returns a chord inverted up a specified number of times.

        Args:
            inversions (int): Number of times to invert up.
        
        Returns: 
            Chord: A new inverted chord.
        """

        new_chord = deepcopy(self)
        new_chord._inversion += inversions
        new_chord._calculate_notes()
        
        return new_chord
    
    def __ilshift__(self, inversions: int) -> "Chord":
        """
        Inverts a chord down by a certain amount of inversions

        Args:
            inversions (int): Number of times to invert down.
        
        Returns:
            Chord: The chord inverted.
        """

        return self.__irshift__(-inversions)

    def __lshift__(self, inversions: int) -> "Chord":
        """
        Returns a chord inverted down a specified number of times.

        Args:
            inversions (int): Number of times to invert up.
        
        Returns:
            Chord: A new inverted chord.
        """

        return self.__rshift__(-inversions)
    
    # Get nth note of chord
    def __getitem__(self, index: int) -> Note:
        """
        Get note of the chord at the specified index.

        Args:
            index (int): Index of note in chord.
        
        Returns: 
            Note: The note at the index.
        """

        return self._notes[index]
    
    def __eq__(self, other: "Chord") -> bool:
        """
        Checks for enharmonic equivalence.

        Args:
            other (Chord): Chord to compare the current chord to.
        
        Returns:
            bool: Whether the two chords are enharmonically equivalent.
        """

        return self._notes == other._notes
    
    def __ne__(self, other: "Chord") -> bool:
        """
        Checks for enharmonic inequivalence.

        Args:
            other (Chord): Chord to compare the current chord to.
        
        Returns:
            bool: Whether the two chords are enharmonically inequivalent.
        """

        return self._notes != other._notes

    def __idiv__(self, note: Note) -> "Chord":
        """
        Turns the chord into a slash chord. Does not support adding a nonexistent note for the bass.

        Args:
            note (Note): Note that will be the bass.
        
        Returns: 
            Chord: The chord with the new bass.

        Raises:
            ValueError: If "note" doesn't exist in the chord.
        """

        for _ in range(len(self._notes)):
            if self[0].letter == note.letter and self[0].accidental == note.accidental:
                return self
             
            self >>= 1
        
        raise ValueError("note doesn't exist in chord")
    
    def __truediv__(self, note: Note) -> "Chord":
        """
        Returns a chord with the specified bass. Does not support adding a nonexistent note for the bass.

        Args:
            note (Note): Note that will be the bass.
        
        Returns:
            Chord: A chord with the new bass.

        Raises:
            ValueError: If "note" doesn't exist in the chord.
        """
        
        test = deepcopy(self)

        for _ in range(len(test._notes)):
            if test[0].letter == note.letter and test[0].accidental == note.accidental:
                return test
             
            test >>= 1
        
        raise ValueError("note doesn't exist in chord")

    # Calculate the notes for the chord from the root, quality, and modifiers
    def _calculate_notes(self):
        self._notes = self._quality._build_core(self._root)

        # Apply modifiers
        for i in range(len(self._modifiers)):
            self._notes = self._modifiers[i]._modify(self._root, self._notes)
        
        # Switch back to major if minor with a missing third or if only note (from no3no5 for some reason)
        if (type(self._quality) == Minor and len(self._notes) >= 2 and nth_letter_from(self._notes[0].letter, 2) != self._notes[1].letter) or (len(self._notes) == 1):
            self._quality = Major()

        # Invert
        self._inversion %= len(self._notes)
        for i in range(self._inversion):
            self._notes.append(self._notes.pop(0))
    
    @property
    def root(self) -> Note:
        """
        Get the root of the chord.

        Returns:
            Note: Root of chord.
        """

        return self._root
    
    @root.setter
    def root(self, new_root: Note):
        """
        Set the root of the chord.

        Args:
            new_root (Note): Note to set the root to.
        """

        self._root = new_root
        self._calculate_notes()
    
    @property
    def quality(self) -> Quality:
        """
        Get the quality of the chord.

        Returns: 
            Quality: Quality of the chord.
        """

        return self._quality
    
    @quality.setter
    def quality(self, new_quality: Quality):
        """
        Set the quality of the chord.

        Args:
            new_quality (Quality): Quality to set the chord to.
        """

        self._quality = new_quality
        self._calculate_notes()
    
    @property
    def inversion(self) -> int:
        """
        Get the inversion of the chord.

        Returns:
            int: Inversion of the chord.
        """

        return self._inversion
    
    @inversion.setter
    def inversion(self, new_inversion):
        """
        Set the inversion of the chord.

        Args:
            new_inversion (int): Inversion to set the chord to.
        """

        self._inversion = new_inversion
        self._calculate_notes()
    
    @property
    def notes(self) -> str:
        """
        Get the notes of the chord.

        Returns: 
            str: Notes of the chord.
        """

        return '-'.join(map(str, self._notes))
    
    @property
    def modifiers(self) -> List[Modifier]:
        """
        Get the modifiers on the chord.

        Returns:
            List[str]: Modifiers on the chord.
        """

        return self._modifiers
    
    @modifiers.setter
    def modifiers(self, new_modifiers):
        """
        Set the modifiers on the chord.

        Returns:
            List[str]: Modifiers on the chord.
        """

        self._modifiers = new_modifiers
        self._calculate_notes()
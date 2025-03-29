from copy import deepcopy
from .roman import Roman
from .quality.base import Quality
from .quality.triad import Major
from .modifier.base import Modifier

class RomanChord:
    """
    Class that represents a chord in Roman numeral analysis.

    Args:
        roman (Roman): Roman numeral of the chord.
        quality (Quality): Quality of the chord.
    """

    def __init__(self, roman: Roman, quality: Quality=Major()):
        self._roman = roman
        self._quality = quality
        self._inversion = 0
        self._modifiers = []
        
        self._target = None
    
    def __repr__(self) -> str:
        s = str(self._roman)

        if str(self._quality) in ("m", "o", "ø"):
            s = s.lower()
        if str(self._quality) != "m":
            s += str(self._quality)

        return s + self._quality._figured_bass(self._inversion) + "".join(str(modifier) for modifier in self._modifiers) + ("/" + str(self._target) if self._target != None else "")

    def __str__(self) -> str:
        s = str(self._roman)

        if str(self._quality) in ("m", "o", "ø"):
            s = s.lower()
        if str(self._quality) != "m":
            s += str(self._quality)

        return s + self._quality._figured_bass(self._inversion) + "".join(str(modifier) for modifier in self._modifiers) + ("/" + str(self._target) if self._target != None else "")
    
    def __idiv__(self, target: "RomanChord") -> "RomanChord":
        """
        Turns the chord into a secondary chord of the specified chord.

        Args:
            target (RomanChord): Chord to build current chord off of.
        
        Returns:
            RomanChord: Secondary chord to target chord.
        """

        if target._roman != Roman(1):
            self._target = target
        else:
            self._target = None

        return self
    
    def __truediv__(self, target: "RomanChord") -> "RomanChord":
        """
        Returns a chord that is the secondary chord of the specified chord.

        Args:
            target (RomanChord): Chord to build current chord off of.
        
        Returns:
            RomanChord: Secondary chord to target chord.
        """

        chord = deepcopy(self)

        if target._roman != Roman(1):
            chord._target = target
        else:
            chord._target = None
        
        return chord
    
    def __irshift__(self, inversions: int) -> "RomanChord":
        """
        Inverts a chord up by a certain amount of inversions

        Args:
            inversions (int): Number of times to invert up.
        
        Returns:
            RomanChord: The chord inverted.
        """

        highest_inversion = len(self.quality._get_integers())
        if len(self._modifiers) > 0 and str(self._modifiers[-1]) in ("no3", "no5"):
            highest_inversion -= 1
        if len(self._modifiers) > 1 and str(self._modifiers[-2]) in ("no3", "no5"):
            highest_inversion -= 1

        self._inversion += inversions
        self._inversion %= highest_inversion
        
        return self

    def __rshift__(self, inversions: int) -> "RomanChord":
        """
        Returns a chord inverted up a specified number of times.

        Args:
            inversions (int): Number of times to invert up.
        
        Returns:
            RomanChord: A new inverted chord.
        """

        new_chord = deepcopy(self)
        
        highest_inversion = len(new_chord.quality._get_integers())
        if len(new_chord._modifiers) > 0 and str(new_chord._modifiers[-1]) in ("no3", "no5"):
            highest_inversion -= 1
        if len(new_chord._modifiers) > 1 and str(new_chord._modifiers[-2]) in ("no3", "no5"):
            highest_inversion -= 1

        new_chord._inversion += inversions
        new_chord._inversion %= highest_inversion
        
        return new_chord
    
    def __ilshift__(self, inversions: int) -> "RomanChord":
        """
        Inverts a chord down by a certain amount of inversions

        Args:
            inversions (int): Number of times to invert down.
        
        Returns:
            RomanChord: The chord inverted.
        """

        return self.__irshift__(-inversions)

    def __lshift__(self, inversions: int) -> "RomanChord":
        """
        Returns a chord inverted down a specified number of times.

        Args:
            inversions (int): Number of times to invert up.
        
        Returns:
            RomanChord: A new inverted chord.
        """

        return self.__rshift__(-inversions)
    
    def attach(self, new_modifier: Modifier) -> "RomanChord":
        """
        Adds a modifier to the Roman chord.

        Args:
            new_modifier: Modifier to add to the Roman chord.

        Returns:
            RomanChord: The Roman chord with the modifier added.
        """

        if new_modifier not in self._modifiers:
            self._modifiers.append(new_modifier)
        self._modifiers = [modifier for modifier in self._modifiers if new_modifier._compatible_with_mod(modifier)]

        return self

    def detach(self, modifier: Modifier) -> "RomanChord":
        """
        Removes a modifier from the Roman chord.

        Args:
            modifier: Modifier to remove from the Roman chord.

        Returns:
            RomanChord: The Roman chord with the modifier removed.
        """

        self._modifiers.remove(modifier)
        return self

    def with_mod(self, new_modifier: Modifier) -> "RomanChord":
        """
        Returns a Roman chord with the supplied modifier.

        Args:
            new_modifier: Modifier to add to the Roman chord.

        Returns:
            RomanChord: A new Roman chord with the modifier added.
        """
        
        new_chord = deepcopy(self)
        if new_modifier not in new_chord._modifiers:
            new_chord._modifiers.append(new_modifier)
        new_chord._modifiers = sorted([modifier for modifier in new_chord._modifiers if new_modifier._compatible_with_mod(modifier)])

        return new_chord            

    def without_mod(self, modifier: Modifier) -> "RomanChord":
        """
        Returns a Roman chord without the supplied modifier.

        Args:
            modifier: Modifier to remove from the Roman chord.

        Returns:
            RomanChord: The Roman chord with the modifier removed.
        """

        new_chord = deepcopy(self)
        new_chord._modifiers.remove(modifier)

        return new_chord
    
    @property
    def roman(self) -> Roman:
        """
        Get Roman numeral of the Roman chord.

        Returns:
            Roman: Roman numeral of the Roman chord.
        """

        return self._roman
    
    @roman.setter
    def roman(self, new_roman: Roman):
        """
        Set Roman numeral of the Roman chord.

        Args:
            new_roman (Roman): Roman numeral to set the Roman chord to.
        """
        
        self._roman = new_roman
    
    @property
    def target(self) -> "RomanChord":
        """
        Get target of secondary chord.

        Returns:
            RomanChord: Target of secondary chord.
        """

        if self._target != None:
            return self._target
        else:
            return RomanChord(Roman(1))
    
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
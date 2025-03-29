from typing import List
from .base import Modifier
from ..note import Note
from ..utils import Accidental, nth_letter_from
from ..quality.extended import *

class Add9(Modifier):
    def __str__(self):
        return "add9"
    
    def __repr__(self):
        return "add9"

    def _get_priority(self) -> int:
        return 6
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("addb9", "add#9", "b9", "#9", "b11", "#11", "b13", "#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return type(quality) not in (Ninth, Eleventh, Thirteenth)

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        letter = nth_letter_from(root.letter, 8)
        new_notes.append(Note(letter, Accidental((14 + int(root) - letter.value) % 12)))

        return new_notes

class AddFlat9(Modifier):
    def __str__(self):
        return "addb9"
    
    def __repr__(self):
        return "addb9"
    
    def _get_priority(self) -> int:
        return 6
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("add9", "add#9", "b9", "#9", "b11", "#11", "b13", "#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return type(quality) not in (Ninth, Eleventh, Thirteenth)

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        letter = nth_letter_from(root.letter, 8)
        new_notes.append(Note(letter, Accidental((13 + int(root) - letter.value) % 12)))

        return new_notes

class AddSharp9(Modifier):
    def __str__(self):
        return "add#9"
    
    def __repr__(self):
        return "add#9"
    
    def _get_priority(self) -> int:
        return 6
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("add9", "addb9", "b9", "#9", "b11", "#11", "b13", "#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return type(quality) not in (Ninth, Eleventh, Thirteenth)

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        letter = nth_letter_from(root.letter, 8)
        new_notes.append(Note(letter, Accidental((15 + int(root) - letter.value) % 12)))

        return new_notes

class Add11(Modifier):
    def __str__(self):
        return "add11"
    
    def __repr__(self):
        return "add11"
    
    def _get_priority(self) -> int:
        return 7
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("addb11", "add#11", "b11", "#11", "b13", "#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return type(quality) not in (Eleventh, Thirteenth)
    
    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        letter = nth_letter_from(root.letter, 10)
        new_notes.append(Note(letter, Accidental((17 + int(root) - letter.value) % 12)))

        return new_notes

class AddFlat11(Modifier):
    def __str__(self):
        return "addb11"
    
    def __repr__(self):
        return "addb11"
    
    def _get_priority(self) -> int:
        return 7
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("add11", "add#11", "b11", "#11", "b13", "#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return type(quality) not in (Eleventh, Thirteenth)

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        letter = nth_letter_from(root.letter, 10)
        new_notes.append(Note(letter, Accidental((16 + int(root) - letter.value) % 12)))

        return new_notes

class AddSharp11(Modifier):
    def __str__(self):
        return "add#11"
    
    def __str__(self):
        return "add#11"
    
    def _get_priority(self) -> int:
        return 7
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("addb11", "add11", "b11", "#11", "b13", "#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return type(quality) not in (Eleventh, Thirteenth)

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        letter = nth_letter_from(root.letter, 10)
        new_notes.append(Note(letter, Accidental((18 + int(root) - letter.value) % 12)))

        return new_notes

class Add13(Modifier):
    def __str__(self):
        return "add13"
    
    def __repr__(self):
        return "add13"
    
    def _get_priority(self) -> int:
        return 8
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("addb13", "add#13", "b13", "#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return type(quality) != Thirteenth

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        letter = nth_letter_from(root.letter, 12)
        new_notes.append(Note(letter, Accidental((21 + int(root) - letter.value) % 12)))

        return new_notes

class AddFlat13(Modifier):
    def __str__(self):
        return "addb13"
    
    def __repr__(self):
        return "addb13"
    
    def _get_priority(self) -> int:
        return 8
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("add13", "add#13", "b13", "#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return type(quality) != Thirteenth

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        letter = nth_letter_from(root.letter, 12)
        new_notes.append(Note(letter, Accidental((20 + int(root) - letter.value) % 12)))

        return new_notes

class AddSharp13(Modifier):
    def __str__(self):
        return "add#13"
    
    def __repr__(self):
        return "add#13"
    
    def _get_priority(self) -> int:
        return 8

    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("add13", "addb13", "b13", "#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return type(quality) != Thirteenth

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        letter = nth_letter_from(root.letter, 12)
        new_notes.append(Note(letter, Accidental((21 + int(root) - letter.value) % 12)))

        return new_notes
from typing import List
from .base import Modifier
from ..note import Note
from ..utils import nth_letter_from

class Flat5(Modifier):
    def __str__(self):
        return "b5"
    
    def __repr__(self):
        return "b5"

    def _get_priority(self) -> int:
        return 0
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("#5", "no5")

    def _compatible_with_quality(self, quality) -> bool:
        return quality.get_integers()[2] != 6

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()
        new_notes[2] = Note.note_relative_to(nth_letter_from(root.letter, 4), root, 6)

        return new_notes

class Sharp5(Modifier):
    def __str__(self):
        return "#5"
    
    def __repr__(self):
        return "#5"
    
    def _get_priority(self) -> int:
        return 0
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("b5", "no5")
    
    def _compatible_with_quality(self, quality) -> bool:
        return quality.get_integers()[2] != 8
    
    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()
        new_notes[2] = Note.note_relative_to(nth_letter_from(root.letter, 4), root, 8)

        return new_notes

class Flat9(Modifier):
    def __str__(self):
        return "b9"
    
    def __repr__(self):
        return "b9"
    
    def _get_priority(self) -> int:
        return 1
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("#9", "add9", "addb9", "add#9")
    
    def _compatible_with_quality(self, quality) -> bool:
        return len(quality.get_integers()) != 3 and len(quality.get_integers()) != 5

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()
        new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 8), root, 13))

        return new_notes

class Sharp9(Modifier):
    def __str__(self):
        return "#9"
    
    def __repr__(self):
        return "#9"
    
    def _get_priority(self) -> int:
        return 1
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("b9", "add9", "addb9", "add#9")
    
    def _compatible_with_quality(self, quality) -> bool:
        return len(quality.get_integers()) != 3 and len(quality.get_integers()) != 5
    
    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()
        new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 8), root, 15))

        return new_notes

class Flat11(Modifier):
    def __str__(self):
        return "b11"
    
    def __repr__(self):
        return "b11"
    
    def _get_priority(self) -> int:
        return 2
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("#11", "add9", "addb9", "add#9", "add11", "addb11", "add#11")
    
    def _compatible_with_quality(self, quality) -> bool:
        return len(quality.get_integers()) != 3 and len(quality.get_integers()) != 6

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        # Add ninth if some kind of ninth doesn't exist
        if not ((int(notes[-1]) - int(root)) % 12 >= 1 and (int(notes[-1]) - int(root)) % 12 <= 3):
            new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 8), root, 14))

        new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 10), root, 16))

        return new_notes

class Sharp11(Modifier):
    def __str__(self):
        return "#11"
    
    def __repr__(self):
        return "#11"
    
    def _get_priority(self) -> int:
        return 2
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("b11", "add9", "addb9", "add#9", "add11", "addb11", "add#11")
    
    def _compatible_with_quality(self, quality) -> bool:
        return len(quality.get_integers()) != 3 and len(quality.get_integers()) != 6

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        # Add ninth if some kind of ninth doesn't exist
        if not ((int(notes[-1]) - int(root)) % 12 >= 1 and (int(notes[-1]) - int(root)) % 12 <= 3):
            new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 8), root, 14))

        new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 10), root, 18))

        return new_notes

class Flat13(Modifier):
    def __str__(self):
        return "b13"
    
    def __repr__(self):
        return "b13"
    
    def _get_priority(self) -> int:
        return 3
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("#13", "add9", "addb9", "add#9", "add11", "addb11", "add#11", "add13", "addb13", "add#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return len(quality.get_integers()) != 3 and len(quality.get_integers()) != 7
    
    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        # Add ninth if some kind of ninth doesn't exist
        if not ((int(notes[-1]) - int(root)) % 12 >= 1 and (int(notes[-1]) - int(root)) % 12 <= 3):
            new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 8), root, 14))
        # Add eleventh if some kind of eleventh doesn't exist
        if not ((int(notes[-1]) - int(root)) % 12 >= 4 and (int(notes[-1]) - int(root)) % 12 <= 6):
            new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 10), root, 17))

        new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 12), root, 20))

        return new_notes

class Sharp13(Modifier):
    def __str__(self):
        return "#13"
    
    def __repr__(self):
        return "#13"
    
    def _get_priority(self) -> int:
        return 3
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) not in ("b13", "add9", "addb9", "add#9", "add11", "addb11", "add#11", "add13", "addb13", "add#13")
    
    def _compatible_with_quality(self, quality) -> bool:
        return len(quality.get_integers()) != 3 and len(quality.get_integers()) != 7

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()

        # Add ninth if some kind of ninth doesn't exist
        if not ((int(notes[-1]) - int(root)) % 12 >= 1 and (int(notes[-1]) - int(root)) % 12 <= 3):
            new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 8), root, 14))
        # Add eleventh if some kind of eleventh doesn't exist
        if not ((int(notes[-1]) - int(root)) % 12 >= 4 and (int(notes[-1]) - int(root)) % 12 <= 6):
            new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 10), root, 17))

        new_notes.append(Note.note_relative_to(nth_letter_from(root.letter, 12), root, 22))

        return new_notes
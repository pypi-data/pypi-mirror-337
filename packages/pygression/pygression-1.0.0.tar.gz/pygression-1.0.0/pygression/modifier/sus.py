from typing import List
from .base import Modifier
from ..note import Note
from ..utils import nth_letter_from, Accidental

class Sus2(Modifier):
    def __str__(self):
        return "sus2"
    
    def __repr__(self):
        return "sus2"
    
    def _get_priority(self) -> int:
        return 4

    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) != "sus4" and str(modifier) != "no3"
    
    def _compatible_with_quality(self, quality) -> bool:
        return True

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()
        new_notes[1] = Note.note_relative_to(nth_letter_from(root.letter, 1), root, 2)
        
        return new_notes

class Sus4(Modifier):
    def __str__(self):
        return "sus4"
    
    def __repr__(self):
        return "sus4"
    
    def _get_priority(self) -> int:
        return 5
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) != "sus2" and str(modifier) != "no3"
        
    def _compatible_with_quality(self, quality) -> bool:
        return True
    
    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()
        new_notes[1] = Note.note_relative_to(nth_letter_from(root.letter, 3), root, 5)

        return new_notes
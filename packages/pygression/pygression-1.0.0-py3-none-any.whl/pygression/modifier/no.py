from typing import List
from .base import Modifier
from ..note import Note
from ..utils import nth_letter_from

class No3(Modifier):
    def __str__(self):
        return "no3"
    
    def __repr__(self):
        return "no3"
    
    def _get_priority(self) -> int:
        return 9
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) != "sus2" and str(modifier) != "sus4"

    def _compatible_with_quality(self, quality) -> bool:
        return True
    
    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()
        
        third = nth_letter_from(root.letter, 2)

        for i in range(len(notes)):
            if new_notes[i].letter == third:
                new_notes.pop(i)
                break

        return new_notes

class No5(Modifier):
    def __str__(self):
        return "no5"
    
    def __repr__(self):
        return "no3"
    
    def _get_priority(self) -> int:
        return 10
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) != "b5" and str(modifier) != "#5"
    
    def _compatible_with_quality(self, quality) -> bool:
        return True

    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        new_notes = notes.copy()
        
        fifth = nth_letter_from(root.letter, 4)

        for i in range(len(notes)):
            if new_notes[i].letter == fifth:
                new_notes.pop(i)
                break

        return new_notes
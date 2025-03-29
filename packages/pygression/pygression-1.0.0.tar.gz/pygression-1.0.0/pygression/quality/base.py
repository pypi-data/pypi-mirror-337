# Dictates how the chord is built
from typing import List
from abc import ABC, abstractmethod
from ..note import Note
from ..utils import nth_letter_from

class Quality(ABC):
    @abstractmethod
    def __str__(self):
        pass
    
    # Notes of the chord as integers
    @staticmethod
    @abstractmethod
    def _get_integers(self) -> List[int]:
        pass
    
    # For Roman numeral analysis
    @abstractmethod
    def _figured_bass(self) -> str:
        pass

    def _build_core(self, root: Note) -> List[Note]:
        notes = []
        integers = self._get_integers()

        for i in range(len(integers)):
            notes.append(Note.note_relative_to(nth_letter_from(root.letter, i * 2), root, integers[i]))

        return notes
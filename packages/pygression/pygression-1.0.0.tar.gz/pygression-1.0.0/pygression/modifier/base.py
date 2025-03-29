from typing import List
from abc import ABC, abstractmethod
from ..note import Note
from ..quality import *

class Modifier(ABC):
    @abstractmethod
    def __str__(self):
        pass
    
    @abstractmethod
    def __repr__(self):
        pass

    def __gt__(self, other):
        return self._get_priority() > other._get_priority()

    def __lt__(self, other):
        return self._get_priority() < other._get_priority()
    
    @abstractmethod
    def _get_priority(self):
        pass
    
    @abstractmethod
    def _compatible_with_mod(self, modifier) -> bool:
        pass
    
    @abstractmethod
    def _compatible_with_quality(self, quality) -> bool:
        pass

    @abstractmethod
    def _modify(self, root: Note, notes: List[Note]) -> List[Note]:
        pass

from typing import List
from .base import Quality

class Ninth(Quality):
    def __str__(self):
        return ""
    
    def _figured_bass(self, inversion: int) -> str:
        return "9"

    @staticmethod
    def _get_integers(self) -> List[int]:
        return [0, 4, 7, 10, 14]
    
class Eleventh(Quality):
    def __str__(self):
        return ""
    
    def _figured_bass(self, inversion: int) -> str:
        return "11"
    
    @staticmethod
    def _get_integers(self) -> List[int]:
        return [0, 4, 7, 10, 14, 17]

class Thirteenth(Quality):
    def __str__(self):
        return ""
    
    def _figured_bass(self, inversion: int) -> str:
        return "13"
    
    @staticmethod
    def _get_integers(self) -> List[int]:
        return [0, 4, 7, 10, 14, 17, 21]
from typing import List
from .base import Quality

class Seventh(Quality):
    def _figured_bass(self, inversion: int) -> str:
        bass = "7"

        if inversion == 1:
            bass = "6/5"
        elif inversion == 2:
            bass = "4/3"
        elif inversion == 3:
            bass = "4/2"

        return bass

class Major(Seventh):
    def __str__(self):
        return "M"

    @staticmethod
    def _get_integers():
        return [0, 4, 7, 11]

class Minor(Seventh):
    def __str__(self):
        return "m"

    @staticmethod
    def _get_integers():
        return [0, 3, 7, 10]

class Dominant(Seventh):
    def __str__(self):
        return ""
    
    @staticmethod
    def _get_integers():
        return [0, 4, 7, 10]

class HalfDiminished(Seventh):
    def __str__(self):
        return "ø"
    
    @staticmethod
    def _get_integers():
        return [0, 3, 6, 10]

class Diminished(Seventh):
    def __str__(self):
        return "o"

    @staticmethod
    def _get_integers():
        return [0, 3, 6, 9]

class MinorMajor(Seventh):
    def __str__(self):
        return "mM"
    
    @staticmethod
    def _get_integers():
        return [0, 3, 7, 11]

class Augmented(Seventh):
    def __str__(self):
        return "+"
    
    @staticmethod
    def _get_integers():
        return [0, 4, 8, 10]

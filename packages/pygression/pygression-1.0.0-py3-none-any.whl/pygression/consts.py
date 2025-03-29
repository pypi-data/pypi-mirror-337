from enum import Enum

class Mode(Enum):
    ION = (0, 2, 4, 5, 7, 9, 11)
    MAJ = (0, 2, 4, 5, 7, 9, 11)
    DOR = (0, 2, 3, 5, 7, 9, 10)
    PHR = (0, 1, 3, 5, 7, 8, 10)
    LYD = (0, 2, 4, 6, 7, 9, 11)
    MIX = (0, 2, 4, 5, 7, 9, 10)
    AEO = (0, 2, 3, 5, 7, 8, 10)
    MIN = (0, 2, 3, 5, 7, 8, 10)
    LOC = (0, 1, 3, 5, 6, 8, 10)
    HMIN = (0, 2, 3, 5, 7, 8, 11)

class Letter(Enum):
    C = 0
    D = 2
    E = 4
    F = 5
    G = 7
    A = 9
    B = 11

class Accidental(Enum):
    NATURAL = 0
    SHARP = 1
    FLAT = -1
    DSHARP = 2
    DFLAT = -2

AS_NOTATION = {
    Letter.C: 'C',
    Letter.D: 'D',
    Letter.E: 'E',
    Letter.F: 'F',
    Letter.G: 'G',
    Letter.A: 'A',
    Letter.B: 'B',
    Accidental.NATURAL: "",
    Accidental.SHARP: "#",
    Accidental.FLAT: "b",
    Accidental.DSHARP: "x",
    Accidental.DFLAT: "bb",
}

ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII")
# pygression

## Overview
pygression is a Python package that adds the ability to represent chord progressions to your code.

## Installation
You can install pygression with pip:
```
python3 -m pip install pygression
```

## Basic Tutorial
The `Note` class is mainly used to get a chord progression in a specific key. It is instantiated with a `Letter` and an optional `Accidental`.
```python
>>> from pygression import Note, Letter, Accidental
>>> note = Note(Letter.A, accidental=Accidental.FLAT)
>>> note
Ab
```

The `Roman` class is needed to create chord progressions that include any kind of chord. It is instantiated with a degree and an optional `Accidental`.
```python
>>> from pygression import Roman
>>> roman = Roman(6, accidental=Accidental.FLAT)
>>> roman
bVI
```

The `RomanChord` class represents chords in Roman numeral analysis. It is instantiated with a `Roman` object and an optional `Quality`.
```python
>>> from pygression import RomanChord
>>> from pygression.quality import triad
>>> rchord = RomanChord(roman, quality=triad.Major())
>>> rchord
bVI
```

The `Progression` class represents chord progressions. Pass in a list of the degrees of the chords or `RomanChord`s in the progression with a mode and how the progression is viewed.
```python
>>> from pygression import Progression, Mode
>>> axis = Progression([1, 5, rchord, 4], mode=Mode.AEO, relative_to=Mode.ION)
>>> axis
[i, v, bVI, iv]
```

To get this progression in a specific key, use the `chords_in` method. This method takes in a `Note` object.
```python
>>> chords = axis.chords_in(note)
>>> chords
[Abm, Ebm, Fb, Dbm]
```

More advanced features can be found in the documentation: https://pygression.readthedocs.io/en/latest/index.html.
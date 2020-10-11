#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from gravon.info  import Info
from gravon.color import Color
from gravon.piece import Piece

from typing import List, Tuple

# page 90 of Vincent de Boer's MSc. thesis:
# http://www.kbs.twi.tudelft.nl/docs/MSc/2007/deBoer/thesis.pdf
symbols = {
    'A': (Info.Empty,   Color.Empty, Piece._E),
    'B': (Info.unknown, Color.red,   Piece._B),
    'C': (Info.unknown, Color.red,   Piece._1),
    'D': (Info.unknown, Color.red,   Piece._2),
    'E': (Info.unknown, Color.red,   Piece._3),
    'F': (Info.unknown, Color.red,   Piece._4),
    'G': (Info.unknown, Color.red,   Piece._5),
    'H': (Info.unknown, Color.red,   Piece._6),
    'I': (Info.unknown, Color.red,   Piece._7),
    'J': (Info.unknown, Color.red,   Piece._8),
    'K': (Info.unknown, Color.red,   Piece._9),
    'L': (Info.unknown, Color.red,   Piece._X),
    'M': (Info.unknown, Color.red,   Piece._F),
    'N': (Info.unknown, Color.blue,  Piece._B),
    'O': (Info.unknown, Color.blue,  Piece._1),
    'P': (Info.unknown, Color.blue,  Piece._2),
    'Q': (Info.unknown, Color.blue,  Piece._3),
    'R': (Info.unknown, Color.blue,  Piece._4),
    'S': (Info.unknown, Color.blue,  Piece._5),
    'T': (Info.unknown, Color.blue,  Piece._6),
    'U': (Info.unknown, Color.blue,  Piece._7),
    'V': (Info.unknown, Color.blue,  Piece._8),
    'W': (Info.unknown, Color.blue,  Piece._9),
    'X': (Info.unknown, Color.blue,  Piece._X),
    'Y': (Info.unknown, Color.blue,  Piece._F),
    '_': (Info.Lake,    Color.Lake,  Piece._L)
}

numbers = { 
    s: n
    for n, s in enumerate(symbols) 
}

def split(field_content: str) -> Tuple[str, str]:
    """
    Split a 100-character field content into a tuple of two 40-character setups.
    """
    assert len(field_content) == 100
    return field_content[:40], field_content[60:][::-1]

def parse(setup: str) -> List[int]:
    """
    Parse a 40-character setup into a list of numbers.
    """
    assert len(setup) == 40
    return [
        numbers[s]
        for s in setup
    ]

def generate(placement: List[int]) -> str:
    """
    Generate a 40-character setup from a list of numbers.
    """
    assert len(placement) == 40
    return ''.join([
        symbols[n]
        for n in placement
    ])

def encode(setup: str, encoding: List[str]) -> str:
    """
    Encode a string of symbols.
    """
    return ''.join([
        encoding[rank]
        for rank in parse(setup)
    ])


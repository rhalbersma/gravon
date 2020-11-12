#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from gravon.piece import Info, Color, Rank, info_labels, color_labels, rank_labels

# page 90 of Vincent de Boer's MSc. thesis:
# http://www.kbs.twi.tudelft.nl/docs/MSc/2007/deBoer/thesis.pdf
symbols = {
    'A': (Info.empty,   Color.empty, Rank.empty),
    'B': (Info.unknown, Color.red,   Rank._B),
    'C': (Info.unknown, Color.red,   Rank._1),
    'D': (Info.unknown, Color.red,   Rank._2),
    'E': (Info.unknown, Color.red,   Rank._3),
    'F': (Info.unknown, Color.red,   Rank._4),
    'G': (Info.unknown, Color.red,   Rank._5),
    'H': (Info.unknown, Color.red,   Rank._6),
    'I': (Info.unknown, Color.red,   Rank._7),
    'J': (Info.unknown, Color.red,   Rank._8),
    'K': (Info.unknown, Color.red,   Rank._9),
    'L': (Info.unknown, Color.red,   Rank._X),
    'M': (Info.unknown, Color.red,   Rank._F),
    'N': (Info.unknown, Color.blue,  Rank._B),
    'O': (Info.unknown, Color.blue,  Rank._1),
    'P': (Info.unknown, Color.blue,  Rank._2),
    'Q': (Info.unknown, Color.blue,  Rank._3),
    'R': (Info.unknown, Color.blue,  Rank._4),
    'S': (Info.unknown, Color.blue,  Rank._5),
    'T': (Info.unknown, Color.blue,  Rank._6),
    'U': (Info.unknown, Color.blue,  Rank._7),
    'V': (Info.unknown, Color.blue,  Rank._8),
    'W': (Info.unknown, Color.blue,  Rank._9),
    'X': (Info.unknown, Color.blue,  Rank._X),
    'Y': (Info.unknown, Color.blue,  Rank._F),
    '_': (Info.lake,    Color.lake,  Rank.lake),
}


def decode_setup(setup: str) -> str:
    return ''.join(
        rank_labels[symbols[piece][2]]
        for piece in setup
    )


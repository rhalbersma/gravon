#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from enum import IntEnum

class Piece(IntEnum):
    _F =  0,
    _1 =  1,
    _2 =  2,
    _3 =  3,
    _4 =  4,
    _5 =  5,
    _6 =  6,
    _7 =  7,
    _8 =  8,
    _9 =  9,
    _X = 10,
    _B = 11,
    _E = 12,
    _L = 13,

piece_labels = [
    Piece(p).name[1]
    for p in Piece
]

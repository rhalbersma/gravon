#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from enum import IntEnum

class Info(IntEnum):
    unknown = 0,
    moved   = 1,
    known   = 2,
    _empty  = 3,
    Lake    = 4,

info_labels = [
    Info(i).name[0]
    for i in Info
]

class Color(IntEnum):
    red    = 0,
    blue   = 1,
    _empty = 2,
    Lake   = 3,

color_labels = [
    Color(c).name[0]
    for c in Color
]

class Rank(IntEnum):
    _F      =  0,
    _1      =  1,
    _2      =  2,
    _3      =  3,
    _4      =  4,
    _5      =  5,
    _6      =  6,
    _7      =  7,
    _8      =  8,
    _9      =  9,
    _X      = 10,
    _B      = 11,
    r_empty = 12,
    _Lake   = 13,

rank_labels = [
    Rank(r).name[1]
    for r in Rank
]

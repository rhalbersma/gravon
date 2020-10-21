#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from enum import IntEnum

class Info(IntEnum):
    unknown = 0,
    moved   = 1,
    known   = 2,
    empty   = 3,
    lake    = 4,

info_labels = [
    Info(i).name[0]
    for i in Info
]
info_labels[Info.empty] = '-'
info_labels[Info.lake ] = '#'

class Color(IntEnum):
    red   = 0,
    blue  = 1,
    empty = 2,
    lake  = 3,

color_labels = [
    Color(c).name[0]
    for c in Color
]
color_labels[Color.empty] = '-'
color_labels[Color.lake ] = '#'

class Rank(IntEnum):
    _F    =  0,
    _1    =  1,
    _2    =  2,
    _3    =  3,
    _4    =  4,
    _5    =  5,
    _6    =  6,
    _7    =  7,
    _8    =  8,
    _9    =  9,
    _X    = 10,
    _B    = 11,
    empty = 12,
    lake  = 13,

rank_labels = [
    Rank(r).name[1]
    for r in Rank
]
rank_labels[Rank.empty] = '-'
rank_labels[Rank.lake ] = '#'
rank_lookup = dict(zip(rank_labels, Rank))

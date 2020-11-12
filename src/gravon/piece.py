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

rank_labels_US = rank_labels.copy()
rank_labels_US[Rank._1] = 'S'
for i, r in zip(reversed(range(1, 10)), range(Rank._2, Rank._B)):
    rank_labels_US[r] = str(i)


def rank_translate(field_content: str, src=rank_labels, dst=rank_labels_US) -> str:
    translate = dict(zip(src, dst))
    return ''.join(translate[rank] for rank in field_content)


rank_lookup = dict(zip(rank_labels, Rank))

rank_names = [
    'flag',
    'spy',
    'scout',
    'miner',
    'sergeant',
    'lieutenant',
    'captain',
    'major',
    'colonel',
    'general',
    'marshal',
    'bomb',
    'empty',
    'lake'
]

rank_counts = {
    'classic' : [ 1, 1, 8, 5, 4, 4, 4, 3, 2, 1, 1, 6,  0, 0 ],
    'ultimate': [ 1, 1, 4, 2, 2, 2, 2, 1, 1, 1, 1, 2, 20, 0 ],
    'duel'    : [ 1, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 2, 30, 0 ],
    'barrage' : [ 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1, 32, 0 ]
}    

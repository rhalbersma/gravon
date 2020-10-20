#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from itertools import product
from typing import List, Tuple

import numpy as np
import pandas as pd

from gravon.piece import Rank, rank_labels, rank_lookup
import gravon.pattern as pattern

H, W = 4, 10

def inner(matrix: np.array) -> np.array:
    return matrix[1:-1, 1:-1]

matrix_init = np.full((H + 2, W + 2), Rank.lake, dtype='int8')
matrix_init[-1, 1: 3] = Rank.empty
matrix_init[-1, 5: 7] = Rank.empty
matrix_init[-1, 9:11] = Rank.empty

inf = 99
dtf_init = np.full((H + 2, W + 2), inf, dtype='int8')
dtf_init[matrix_init == Rank.empty] = -1

row_labels = [ str(row +        1) for row in range(H) ]
col_labels = [ chr(col + ord('a')) for col in range(W) ]

def neighbors_idx(r: int, c: int) -> Tuple[Tuple[int, int]]:
    assert (1 <= r <= H) and (1 <= c <= W)
    return (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)

def neighbors_mat(m: np.array, r: int, c: int) -> Tuple:
    return tuple(
        m[sq]
        for sq in neighbors_idx(r, c)
    )

def rank_counts(type='classic') -> List[int]:
    return {
        'classic' : [ 1, 1, 8, 5, 4, 4, 4, 3, 2, 1, 1, 6,  0, 0 ],
        'ultimate': [ 1, 1, 4, 2, 2, 2, 2, 1, 1, 1, 1, 2, 20, 0 ],
        'duel'    : [ 1, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 2, 30, 0 ],
        'barrage' : [ 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1, 32, 0 ]
    }[type]

lanes = np.array((3 * [ 'L' ] + 4 * [ 'M' ] + 3 * [ 'R' ]) * 4).reshape(H, W)
lanes[0:2, :] = '_'
lanes[3, 4:6] = '_'

class Setup:
    def __init__(self, setup: str, type='classic'):
        assert len(setup) == H * W
        self.matrix = matrix_init.copy()
        self.matrix[1:-1, 1:-1] = np.array([
            rank_lookup[piece]
            for piece in setup
        ]).reshape((H, W))
        self.type = type

    def __str__(self) -> str:
        return ''.join([
            rank_labels[piece] 
            for piece in inner(self.matrix).flatten() 
        ])

    def ok(self) -> bool:
        return (
            dict(zip(*np.unique(inner(self.matrix), return_counts=True))) ==
            dict(list(filter(lambda item: item[1] > 0, zip(Rank, rank_counts(self.type)))))
        )

    def piece_label(self, r: int, c: int) -> str:
        assert (1 <= r <= H) and (1 <= c <= W)
        return rank_labels[self.matrix[r, c]] + col_labels[c - 1] + row_labels[r - 1]

    def h1(self) -> np.array:
        """
        Distance to freedom
        """
        flag_or_bomb = np.isin(self.matrix, (Rank._F, Rank._B))
        dtf = dtf_init.copy()
        level = -1
        assert np.sum(dtf == level) > 0
        while True:
            updated = dtf.copy()
            for r in range(1, H + 1):
                for c in range(1, W + 1):
                    if (not flag_or_bomb[r, c]) and (dtf[r, c] > level) and (level in neighbors_mat(dtf, r, c)):
                        updated[r, c] = level + 1
            dtf = updated
            level += 1
            if np.sum(dtf == level) == 0:
                break
        updated = dtf.copy()
        for r in range(1, H + 1):
            for c in range(1, W + 1):
                if flag_or_bomb[r, c]:
                    updated[r, c] = min(1 + min(neighbors_mat(dtf, r, c)), inf)
        self.dtf = updated    
        return inner(self.dtf)

    def h2(self) -> Tuple[List[str]]:
        """"
        Pieces surrounded by bombs
        """
        self.surrounded = [ 
            self.piece_label(r, c) 
            for r, c in map(tuple, np.transpose(np.where(
                self.dtf == inf
            )))
            if (1 <= r <= H) and (1 <= c <= W)
        ]
        self.partially_surrounded = [
            self.piece_label(r, c) 
            for r, c in map(tuple, np.transpose(np.where(
                (inner(self.dtf) > 5) & (inner(self.dtf) != inf)
            )))
        ]
        return self.surrounded, self.partially_surrounded

    def h3(self) -> bool:
        """"
        Flag Bombed in
        """
        return any(map(lambda p: p.startswith('F'), self.surrounded))

    def h4(self) -> List[int]:
        """
        Flag defense
        """
        flag_side = lanes[2, np.where(inner(self.matrix) == Rank._F)[1]]
        return np.sort(inner(self.matrix)[lanes == flag_side])

    def h5(self) -> List[str]:
        """"
        Pieces blocked by the spy
        """
        spy = tuple(np.transpose(np.where(self.matrix == Rank._1))[0])
        blocked_by_spy = [
            self.piece_label(r, c)
            for r, c in neighbors_idx(*spy)
            if self.dtf[r, c] > self.dtf[spy]
        ]
        return blocked_by_spy 

    def h6(self) -> List[str]:
        """"
        Pieces blocked by a slightly lower piece
        """
        blocking_higher = [
            self.piece_label(r, c)
            for r, c in product(range(1, H + 1), range(1, W + 1))
            if any([(
                    (self.matrix[r, c] in range(2, 9)) and
                    (self.matrix[n] - self.matrix[r, c] in (1, 2)) and
                    (1 < self.dtf[r, c] < self.dtf[n])
                )
                for n in neighbors_idx(r, c)
            ])
        ]
        blocked_by_lower = [
            self.piece_label(r, c)
            for r, c in product(range(1, H + 1), range(1, W + 1))
            if any([(
                    (self.matrix[n] in range(2, 9)) and
                    (self.matrix[r, c] - self.matrix[n] in (1, 2)) and
                    (1 < self.dtf[n] < self.dtf[r, c])
                )
                for n in neighbors_idx(r, c)
            ])
        ]
        return blocking_higher, blocked_by_lower

    def h7(self) -> List[str]:
        """
        Miners on the front row
        """
        front_row_miners = [
            self.piece_label(r, c)
            for r, c in map(tuple, np.transpose(np.where(
                (self.matrix == Rank._3) & (self.dtf == 0)
            )))
        ]
        return front_row_miners

    def h8(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Bomb protection
        """
        spy_or_scout = map(tuple, np.transpose(np.where(
            np.isin(self.matrix, (Rank._1, Rank._2))
        )))
        bomb_weakeners = [
            self.piece_label(r, c)
            for r, c in spy_or_scout
            for n in neighbors_idx(r, c)
            if self.matrix[n] == Rank._B
        ]
        bombs = map(tuple, np.transpose(np.where(
            self.matrix == Rank._B
        )))
        strong_bombs = [
            self.piece_label(r, c)
            for r, c in bombs
            if any([
                np.isin(self.matrix[n], (Rank._4, Rank._5))
                for n in neighbors_idx(r, c)
            ])        
        ]
        flag_bombs = [
            self.piece_label(r, c)
            for r, c in bombs
            if any([
                self.matrix[n] == Rank._F
                for n in neighbors_idx(r, c)
            ])        
        ]
        weak_flag_bombs = list(set(flag_bombs) - set(strong_bombs))
        return bomb_weakeners, strong_bombs, weak_flag_bombs

    def h9(self):
        """
        Starting pieces
        """
        starting_pieces = dict(zip(*np.unique(inner(self.matrix)[inner(self.dtf) < 2], return_counts=True)))
        return sum(starting_pieces.values()), starting_pieces

vdb = [
    """
    6225263X26
    54B1927782
    4B4785B564
    23B23BFB33
    """,
    """
    X653262226
    4288924BB5
    727165B452
    73334BFBB3
    """,
    """
    6249622X26
    5275B27783
    4813B2655B
    3B4B4233BF
    """,
    """
    2852629326
    X27826B5B5
    647175B4B4
    32334BFB32
    """,
    """
    9624222362
    3287B5X758
    B6175265B4
    423B433BFB
    """,
    """
    2659262X62
    72B1842784
    54B273565B
    3B423B33BF
    """
]

scores = [ 18, 18, 20, 22, 19, 16 ]

df = (pd
    .DataFrame(
        data=list(map(lambda s: Setup(pattern.serial(s)), vdb)),
        columns=['setup']
    ).assign(
        ok = lambda r: r.setup.apply(lambda x: x.ok()),
        h1 = lambda r: r.setup.apply(lambda x: x.h1()),
        h2 = lambda r: r.setup.apply(lambda x: x.h2()),
        h3 = lambda r: r.setup.apply(lambda x: x.h3()),
        h4 = lambda r: r.setup.apply(lambda x: x.h4()),
        h5 = lambda r: r.setup.apply(lambda x: x.h5()),
        h6 = lambda r: r.setup.apply(lambda x: x.h6()),
        h7 = lambda r: r.setup.apply(lambda x: x.h7()),
        h8 = lambda r: r.setup.apply(lambda x: x.h8()),
        h9 = lambda r: r.setup.apply(lambda x: x.h9())
    )
    .drop(columns='h1')
)

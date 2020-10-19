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

matrix_e0 = np.full((H + 2, W + 2), Rank.lake, dtype='int8')
matrix_e0[H + 1, 1: 3] = Rank.empty
matrix_e0[H + 1, 5: 7] = Rank.empty
matrix_e0[H + 1, 9:11] = Rank.empty

inf = 99
dtf_e0 = np.full((H + 2, W + 2), inf, dtype='int8')
dtf_e0[matrix_e0 == Rank.empty] = -1

row_labels = [ str(row +        1) for row in range(H) ]
col_labels = [ chr(col + ord('a')) for col in range(W) ]

def neighbors_idx(r: int, c: int) -> Tuple[Tuple[int, int]]:
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
        self.matrix = np.array([
            rank_lookup[piece]
            for piece in setup
        ]).reshape((H, W))
        self.type = type

    def __str__(self) -> str:
        return ''.join([
            rank_labels[piece] 
            for piece in self.matrix.flatten() 
        ])

    def is_legal(self) -> bool:
        return \
            dict(zip(*np.unique(self.matrix, return_counts=True))) == \
            dict(list(filter(lambda item: item[1] > 0, zip(Rank, rank_counts(self.type)))))

    def h1(self) -> np.array:
        """
        Distance to freedom
        """
        self.matrix_e = matrix_e0.copy()
        self.matrix_e[1:(H + 1), 1:(W + 1)] = self.matrix
        flag_or_bomb = np.isin(self.matrix_e, (Rank._F, Rank._B))
        dtf_e = dtf_e0.copy()
        level = -1
        assert np.sum(dtf_e == level) > 0
        while True:
            updated = dtf_e.copy()
            for r in range(1, H + 1):
                for c in range(1, W + 1):
                    if (not flag_or_bomb[r, c]) and (dtf_e[r, c] > level) and (level in neighbors_mat(dtf_e, r, c)):
                        updated[r, c] = level + 1
            dtf_e = updated
            level += 1
            if np.sum(dtf_e == level) == 0:
                break
        updated = dtf_e.copy()
        for r in range(1, H + 1):
            for c in range(1, W + 1):
                if flag_or_bomb[r, c]:
                    updated[r, c] = min(1 + min(neighbors_mat(dtf_e, r, c)), inf)
        self.dtf_e = updated    
        self.dtf = self.dtf_e[1:(H + 1), 1:(W + 1)]
        return self.dtf

    def h2(self) -> Tuple[List[str]]:
        """"
        Pieces surrounded by bombs
        """
        self.surrounded = [ 
            rank_labels[self.matrix[r, c]] + col_labels[c] + row_labels[r] 
            for r, c in map(tuple, np.transpose(np.where(
                self.dtf == inf
            )))
        ]
        self.partially_surrounded = [
            rank_labels[self.matrix[r, c]] + col_labels[c] + row_labels[r] 
            for r, c in map(tuple, np.transpose(np.where(
                (self.dtf > 5) & (self.dtf != inf)
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
        flag_side = lanes[2, np.where(self.matrix == Rank._F)[1]]
        self.flag_defense = self.matrix[lanes == flag_side]
        return np.sort(self.flag_defense)

    def h5(self) -> List[str]:
        """"
        Pieces blocked by the spy
        """
        spy = tuple(np.transpose(np.where(self.matrix_e == Rank._1))[0])
        self.blocked_by_spy = [
            rank_labels[self.matrix_e[r, c]] + col_labels[c - 1] + row_labels[r - 1]
            for r, c in neighbors_idx(*spy)
            if self.dtf_e[r, c] > self.dtf_e[spy]
        ]
        return self.blocked_by_spy 

    def h6(self) -> List[str]:
        """"
        Pieces blocked by a slightly lower piece
        """
        self.blocking_higher = [
            rank_labels[self.matrix_e[r, c]] + col_labels[c - 1] + row_labels[r - 1]
            for r, c in product(range(1, H + 1), range(1, W + 1))
            if any([(
                    (self.matrix_e[r, c] in range(2, 9)) and
                    (self.matrix_e[n] - self.matrix_e[r, c] in (1, 2)) and
                    (1 < self.dtf_e[r, c] < self.dtf_e[n])
                )
                for n in neighbors_idx(r, c)
            ])
        ]
        self.blocked_by_lower = [
            rank_labels[self.matrix_e[r, c]] + col_labels[c - 1] + row_labels[r - 1]
            for r, c in product(range(1, H + 1), range(1, W + 1))
            if any([(
                    (self.matrix_e[n] in range(2, 9)) and
                    (self.matrix_e[r, c] - self.matrix_e[n] in (1, 2)) and
                    (1 < self.dtf_e[n] < self.dtf_e[r, c])
                )
                for n in neighbors_idx(r, c)
            ])
        ]
        return self.blocking_higher, self.blocked_by_lower

    def h7(self) -> List[str]:
        """
        Miners on the front row
        """
        self.front_row_miners = [
            rank_labels[self.matrix[r, c]] + col_labels[c] + row_labels[r]
            for r, c in map(tuple, np.transpose(np.where(
                (self.matrix == Rank._3) & (self.dtf == 0)
            )))
        ]
        return self.front_row_miners

    def h8(self) -> List[str]:
        spy_or_scout = map(tuple, np.transpose(np.where(
            np.isin(self.matrix_e, (Rank._1, Rank._2))
        )))
        bomb_weakeners = [
            rank_labels[self.matrix_e[r, c]] + col_labels[c - 1] + row_labels[r - 1]
            for r, c in spy_or_scout
            for n in neighbors_idx(r, c)
            if self.matrix_e[n] == Rank._B
        ]

        return bomb_weakeners

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
        is_legal = lambda r: r.setup.apply(lambda x: x.is_legal()),
        h1 = lambda r: r.setup.apply(lambda x: x.h1()),
        h2 = lambda r: r.setup.apply(lambda x: x.h2()),
        h3 = lambda r: r.setup.apply(lambda x: x.h3()),
        h4 = lambda r: r.setup.apply(lambda x: x.h4()),
        h5 = lambda r: r.setup.apply(lambda x: x.h5()),
        h6 = lambda r: r.setup.apply(lambda x: x.h6()),
        h7 = lambda r: r.setup.apply(lambda x: x.h7()),
        h8 = lambda r: r.setup.apply(lambda x: x.h8())
    )
    .drop(columns='h1')
)

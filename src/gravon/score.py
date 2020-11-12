#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import itertools
from typing import List, Tuple

import numpy as np
import pandas as pd

import gravon.pattern as pattern
from gravon.piece import Rank, rank_labels, rank_lookup
from gravon.setup import Setup, H, W, inner

inf = 99
dtf_init = np.full((H + 2, W + 2), inf, dtype='int8')
dtf_init[Setup.rank_init == Rank.empty] = -1

row_labels = [ str(row +        1) for row in range(H) ]
col_labels = [ chr(col + ord('a')) for col in range(W) ]

Square = Tuple[int, int]


def squares_where(condition: np.array) -> List[Square]:
    return list(map(tuple, np.transpose(np.where(condition))))


def neighbors(sq: Square) -> Tuple[Square]:
    r, c = sq
    assert (1 <= r <= H) and (1 <= c <= W)
    return (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)


def neighbors_mat(m: np.array, sq: Square) -> Tuple:
    return tuple(
        m[nb]
        for nb in neighbors(sq)
    )


lanes = np.array((3 * [ 'L' ] + 4 * [ 'M' ] + 3 * [ 'R' ]) * 4).reshape(H, W)
lanes[0:2, :] = '_'
lanes[3, 4:6] = '_'


class Eval(Setup):
    def __init__(self, **kw):
        super.__init__(self, **kw)

    def __str__(self) -> str:
        return ''.join(
            rank_labels[r] 
            for r in inner(self.rank).flatten() 
        )

    def piece_label(self, sq: Square) -> str:
        r, c = sq
        assert (1 <= r <= H) and (1 <= c <= W)
        return rank_labels[self.rank[r, c]] + col_labels[c - 1] + row_labels[r - 1]

    def h1(self) -> np.array:
        """
        Distance to freedom
        """
        _FB = np.isin(self.rank, (Rank._F, Rank._B))
        dtf = dtf_init.copy()
        level = -1
        assert np.sum(dtf == level) > 0
        while True:
            updated = dtf.copy()
            for sq in setup_area():
                if (not _FB[sq]) and (dtf[sq] > level) and (level in neighbors_mat(dtf, sq)):
                    updated[sq] = level + 1
            dtf = updated
            level += 1
            if np.sum(dtf == level) == 0:
                break
        updated = dtf.copy()
        for sq in setup_area():
            if _FB[sq]:
                updated[sq] = min(1 + min(neighbors_mat(dtf, sq)), inf)
        self.dtf = updated    
        return inner(self.dtf)

    def h2(self) -> Tuple[List[str]]:
        """
        Pieces surrounded by bombs
        """
        dtf_inf = [ 
            self.piece_label(sq) 
            for sq in squares_where(
                (self.dtf == inf) & (self.rank != Rank.lake)
            )
        ]
        dtf_gt5 = [
            self.piece_label(sq) 
            for sq in squares_where(
                (self.dtf > 5) & (self.dtf != inf)
            )
        ]
        return dtf_inf, dtf_gt5

    def h3(self) -> bool:
        """
        Flag Bombed in
        """
        return [
            self.piece_label(sq) 
            for sq in squares_where(
                (self.dtf == inf) & (self.rank == Rank._F)
            )
        ]

    def h4(self) -> List[int]:
        """
        Flag defense
        """
        flag_side = lanes[2, np.where(inner(self.rank) == Rank._F)[1]]
        return np.sort(inner(self.rank)[lanes == flag_side])

    def h5(self) -> List[str]:
        """
        Pieces blocked by the spy
        """
        ge7_blocked_by_1 = [
            self.piece_label(nb)
            for _1 in squares_where(self.rank == Rank._1)
            for nb in neighbors(_1)
            if (self.rank[nb] >= Rank._7) and (self.dtf[nb] > self.dtf[_1])
        ]
        return ge7_blocked_by_1

    def h6(self) -> List[str]:
        """
        Pieces blocked by a slightly lower piece
        """
        blocking_12higher = [
            self.piece_label(sq)
            for sq in setup_area()
            if any([(
                    (self.rank[sq] in range(2, 9)) and
                    (self.rank[nb] - self.rank[sq] in (1, 2)) and
                    (1 < self.dtf[sq] < self.dtf[nb])
                )
                for nb in neighbors(sq)
            ])
        ]
        blocked_by_12lower = [
            self.piece_label(sq)
            for sq in setup_area()
            if any([(
                    (self.rank[nb] in range(2, 9)) and
                    (self.rank[sq] - self.rank[nb] in (1, 2)) and
                    (1 < self.dtf[nb] < self.dtf[sq])
                )
                for nb in neighbors(sq)
            ])
        ]
        return blocking_12higher, blocked_by_12lower

    def h7(self) -> List[str]:
        """
        Miners on the front row
        """
        _3_front = [
            self.piece_label(_3)
            for _3 in squares_where(
                (self.rank == Rank._3) & (self.dtf <= 1)
            )
        ]
        return _3_front

    def h8(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Bomb protection
        """
        _12_B = [
            self.piece_label(_12)
            for _12 in squares_where(np.isin(self.rank, (Rank._1, Rank._2)))
            if any([
                self.rank[nb] == Rank._B
                for nb in neighbors(_12)
            ])
        ]
        _Bs = squares_where(self.rank == Rank._B)
        _B_45 = [
            self.piece_label(_B)
            for _B in _Bs
            if any([
                self.rank[nb] in (Rank._4, Rank._5)
                for nb in neighbors(_B)
            ])        
        ]
        _B_F = [
            self.piece_label(_B)
            for _B in _Bs
            if any([
                self.rank[nb] == Rank._F
                for nb in neighbors(_B)
            ])        
        ]
        weak_flag_bombs = list(set(_B_F) - set(_B_45))
        #return _12_B, _B_45, _B_F, weak_flag_bombs
        return _12_B, _B_45, _B_F, weak_flag_bombs

    def h9(self):
        """
        Starting pieces
        """
        starting_pieces = dict(zip(*np.unique(inner(self.rank)[inner(self.dtf) < 2], return_counts=True)))
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
        data=list(map(lambda s: Setup(pattern.pat1d_identity(s)), vdb)),
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

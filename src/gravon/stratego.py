#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np

from . import pieces

class SetupBoard:
    W, H = 10, 4

    counts = {
        'classic' : [ 1, 1, 8, 5, 4, 4, 4, 3, 2, 1, 1, 6 ],
        'barrage' : [ 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1 ],
        'duell'   : [ 1, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 2 ],
        'ultimate': [ 1, 1, 4, 2, 2, 2, 2, 1, 1, 1, 1, 2 ]
    }

    lane_cols = [ list(range(0, 3)), list(range(3, 7)), list(range(7, 10)) ]
    lane_char = [ 'L', 'M', 'R' ]
    side_cols = [ list(range(0, 5)), list(range(5, 10)) ]
    side_char = [ 'L', 'R' ]

    def __init__(self, setup: str, piece_fmt: str='EU', game_type: str='classic') -> None:
        assert len(setup) == self.W * self.H
        self.chars = pieces.chars[piece_fmt]
        self.unique = [ self.chars[u] for u in pieces.unique_ranks ]
        self.matrix = np.array([ piece for piece in setup ]).reshape(self.H, self.W)
        self.tensor = np.array([ self.matrix == piece for piece in self.chars ]).astype(int)
        self.game_type = game_type
        assert setup == str(self)
        assert self.is_legal()

    def is_legal(self) -> bool:
        return dict(zip(*np.unique(self.matrix, return_counts=True))) == dict(zip(self.chars, self.counts[self.game_type]))

    def __str__(self) -> str:
        return ''.join(self.matrix.flatten())

    def diagram(self, col_sep: str=' ') -> str:
        return '\n'.join(col_sep.join(str(piece) for piece in row) for row in np.flip(self.matrix, axis=0))

    def where(self, piece: str='F') -> list:
        assert piece in self.unique
        loc = np.argwhere(self.matrix == piece)
        assert len(loc) == 1
        return loc[0]

    def lane(self, piece: str='F') -> str:
        assert piece in self.unique
        column = self.where(piece)[1]
        return self.lane_char[ [ column in lane for lane in self.lane_cols ].index(True) ]

    def side(self, piece: str='F') -> str:
        assert piece in self.unique
        column = self.where(piece)[1]
        return self.side_char[ [ column in side for side in self.side_cols ].index(True) ]

    def mirror(self):
        self.matrix = np.flip(self.matrix, axis=1)
        return self

    def canonical(self, dst_side: str='L', piece: str='F'):
        assert piece in self.unique
        src_side = self.side(piece)
        return (self, True) if dst_side == src_side else (self.mirror(), False)

    def square(self, sq: str):
        row = int(sq[1:]) - 1
        col = ord(sq[0]) - ord('a')
        return self.matrix[row, col]

    def row_sums(self, rank: int=None) -> np.array:
        if rank == None:
            return np.sum(self.tensor, axis=2)
        else:
            return np.sum(self.tensor[rank,:,:], axis=1)

    def col_sums(self, rank: int=None) -> np.array:
        if rank == None:
            return np.sum(self.tensor, axis=1)
        else:
            return np.sum(self.tensor[rank,:,:], axis=0)

    def lane_sums(self, rank: int=None) -> np.array:
        s = self.col_sums(rank)
        if rank == None:
            return np.array([ np.sum(s[:,lane], axis=1) for lane in self.lane_cols ]).transpose()
        else:
            return np.array([ np.sum(s[lane])           for lane in self.lane_cols ])

    def side_sums(self, rank: int=None) -> np.array:
        s = self.col_sums(rank)
        if rank == None:
            return np.array([ np.sum(s[:,side], axis=1) for side in self.side_cols ]).transpose()
        else:
            return np.array([ np.sum(s[side])           for side in self.side_cols ])

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np

from . import pieces

class Setup:
    W, H = 10, 4

    counts = {
        'classic' : [ 1, 1, 8, 5, 4, 4, 4, 3, 2, 1, 1, 6 ],
        'barrage' : [ 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1 ],
        'duell'   : [ 1, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 2 ],
        'ultimate': [ 1, 1, 4, 2, 2, 2, 2, 1, 1, 1, 1, 2 ]
    }

    def __init__(self, setup: str, fmt: str='EU', game_type: str='classic'):
        assert len(setup) == self.W * self.H
        self.encoding = pieces.encoding[fmt]
        self.unique_pieces = [ self.encoding[u] for u in pieces.unique_ranks ]
        self.matrix = np.array([ piece for piece in setup ]).reshape(self.H, self.W)
        self.tensor = np.array([ self.matrix == piece for piece in self.encoding ]).astype(int)
        self.game_type = game_type
        assert setup == str(self)
        assert self.is_legal()

    def is_legal(self) -> bool:
        return dict(zip(*np.unique(self.matrix, return_counts=True))) == dict(zip(self.encoding, self.counts[self.game_type]))

    def __str__(self) -> str:
        return ''.join(self.matrix.flatten())

    def diagram(self) -> str:
        return '\n'.join(''.join(str(piece) for piece in row) for row in np.flip(self.matrix, axis=0))

    def where(self, unique_piece: str='F') -> list:
        assert unique_piece in self.unique_pieces
        loc = np.argwhere(self.matrix == unique_piece)
        assert len(loc) == 1
        return loc[0]

    def side(self, unique_piece: str='F') -> str:
        assert unique_piece in self.unique_pieces
        loc = np.argwhere(self.matrix == unique_piece)
        assert len(loc) == 1
        column = loc[0][1]
        return 'L' if column in range(self.W // 2) else 'R'

    def mirror(self):
        self.matrix = np.flip(self.matrix, axis=1)
        return self

    def canonical(self, dst_side: str='L', unique_piece: str='F'):
        assert unique_piece in self.unique_pieces
        src_side = self.side(unique_piece)
        return (self, True) if dst_side == src_side else (self.mirror(), False)

    def square(self, sq: str):
        col = ord(sq[0]) - ord('a')
        row = int(sq[1:]) - 1
        return self.matrix[row, col]

    def rdist(self, p: str) -> str:
        return ''.join([str(i) for i in np.sum(self.matrix == p, axis=1)])

    def cdist(self, p: str) -> str:
        return ''.join([str(i) for i in np.sum(self.matrix == p, axis=0)])

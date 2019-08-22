#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np

class Setup:
    W, H = 10, 4

    pieces = [ 'F' ] + [ str(i) for i in range(1, 10) ] + [ 'X', 'B' ]

    ranks = { piece : rank for rank, piece in enumerate(pieces) }

    counts = {
        'classic' : [ 1, 1, 8, 5, 4, 4, 4, 3, 2, 1, 1, 6 ],
        'barrage' : [ 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1 ]
    }

    def __init__(self, setup: str, game_type: str='classic'):
        assert len(setup) == self.W * self.H
        self.board = np.array([ piece for piece in setup ]).reshape(self.H, self.W)
        self.tensor = np.array([ self.board == piece for piece in self.pieces ]).astype(int)
        self.game_type = game_type
        assert setup == str(self)
        assert self.is_legal()

    def is_legal(self) -> bool:
        return dict(zip(*np.unique(self.board, return_counts=True))) == dict(zip(self.pieces, self.counts[self.game_type]))

    def __str__(self) -> str:
        return ''.join(self.board.flatten())

    def diagram(self) -> str:
        return np.array2string(np.flip(self.board, axis=0))

    def side(self, unique_piece: str='F') -> str:
        column = np.where(self.board == unique_piece)[1]
        assert len(column) == 1
        return 'L' if column in range(self.W // 2) else 'R'

    def mirror(self):
        self.board = np.flip(self.board, axis=1)
        return self

    def canonical(self, dst_side: str='L', unique_piece: str='F'):
        src_side = self.side(unique_piece)
        return (self, True) if dst_side == src_side else (self.mirror(), False)

    def square(self, sq: str):
        col = ord(sq[0]) - ord('a')
        row = int(sq[1]) - 1
        return self.board[row, col]

    def rdist(self, p: str) -> str:
        return ''.join([str(i) for i in np.sum(self.board == p, axis=1)])

    def cdist(self, p: str) -> str:
        return ''.join([str(i) for i in np.sum(self.board == p, axis=0)])

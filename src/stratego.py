#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np

import strados2

class Setup:
    W, H = 10, 4

    def __init__(self, s: str, game_type: str='classic', encoding=strados2.Encode()):
        assert len(s) == self.W * self.H
        self.pieces = np.array([ c for c in s ]).reshape(self.H, self.W)
        assert s == self.strados2()
        self.piece_count = dict(zip(*np.unique(self.pieces, return_counts=True)))
        if game_type == 'classic':
            assert self.piece_count == dict(zip(encoding.pieces, encoding.classic))
        elif game_type == 'barrage':
            assert self.piece_count == dict(zip(encoding.pieces, encoding.barrage))

    def __str__(self) -> str:
        return np.array2string(np.flip(self.pieces, axis=0))

    def strados2(self) -> str:
        return ''.join(self.pieces.flatten())

    def side(self, unique_piece: str='F') -> str:
        column = np.where(self.pieces == unique_piece)[1]
        assert len(column) == 1
        return 'L' if column in range(self.W // 2) else 'R'

    def mirror(self):
        self.pieces = np.flip(self.pieces, axis=1)
        return self

    def canonical(self, dst_side: str='L', unique_piece: str='F'):
        src_side = self.side(unique_piece)
        return (self, True) if dst_side == src_side else (self.mirror(), False)

    def square(self, sq: str):
        f = ord(sq[0]) - ord('a')
        r = int(sq[1]) - 1
        return self.pieces[r, f]

    def rdist(self, p: str) -> str:
        return ''.join([str(i) for i in np.sum(self.pieces == p, axis=1)])

    def cdist(self, p: str) -> str:
        return ''.join([str(i) for i in np.sum(self.pieces == p, axis=0)])

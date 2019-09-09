#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

class Piece:
    def chars(piece_fmt: str='EU') -> list:
        switch = {
            'EU': [ 'F' ] + [ str(i) for i in range(1, 10) ] + [ 'X', 'B' ],
            'US': [ 'F', 'S' ] + [ str(i) for i in reversed(range(1, 10)) ] + [ 'B' ]
        }
        return switch.get(piece_fmt, piece_fmt)

    def counts(game_type: str='classic') -> list:
        switch = {
            'classic' : [ 1, 1, 8, 5, 4, 4, 4, 3, 2, 1, 1, 6 ],
            'barrage' : [ 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1 ],
            'duell'   : [ 1, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 2 ],
            'ultimate': [ 1, 1, 4, 2, 2, 2, 2, 1, 1, 1, 1, 2 ]
        }
        return switch.get(game_type, game_type)

    def names() -> list:
        return [ 'flag', 'spy', 'scout', 'miner', 'sergeant', 'lieutenant', 'captain', 'major', 'colonel', 'general', 'marshal', 'bomb' ]

    def ranks(piece_fmt: str='EU') -> list:
        switch = { fmt : dict(zip(chars(piece_fmt), range(12))) for fmt in [ 'EU', 'US' ] }
        return switch.get(piece_fmt, piece_fmt)

    def translate(piece_char: str, src_fmt: str='EU', dst_fmt: str='US') -> str:
        assert len(piece_char) == 1
        switch = dict(zip(chars(src_fmt), chars(dst_fmt)))
        return switch.get(piece_char, piece_char)

    def unique_ranks() -> list:
        return [ 0, 1, 9, 10 ]

class Board:
    shape = (4, 10)

    lane_cols = [ list(range(0, 3)), list(range(3, 7)), list(range(7, 10)) ]
    lane_char = [ 'L', 'M', 'R' ]
    side_cols = [ list(range(0, 5)), list(range(5, 10)) ]
    side_char = [ 'L', 'R' ]

    def __init__(self, setup: str, piece_fmt: str='EU', game_type: str='classic') -> None:
        assert len(setup) == self.Rows * self.Columns
        self.chars = Piece.chars(piece_fmt)
        self.unique = [ self.chars[u] for u in Piece.unique_ranks() ]
        self.string = setup
        self.matrix = np.array(list(self.string)).reshape(self.shape)
        self.tensor = np.array([ self.matrix == piece for piece in self.chars ]).astype(int)
        self.game_type = game_type
        assert self.is_legal()

    def is_legal(self) -> bool:
        return dict(zip(*np.unique(self.matrix, return_counts=True))) == dict(zip(self.chars, Piece.counts(self.game_type)))

    def __str__(self) -> str:
        return self.string

    def diagram(self, sep: str=' ') -> str:
        return '\n'.join(sep.join(str(piece) for piece in row) for row in np.flip(self.matrix, axis=0))

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

    def mirror(self) -> Board:
        self.matrix = np.flip(self.matrix, axis=1)
        return self

    def canonical(self, dst_side: str='L', piece: str='F') -> Board:
        assert piece in self.unique
        src_side = self.side(piece)
        return (self, True) if dst_side == src_side else (self.mirror(), False)

    def square(self, sq: str) -> str:
        row = ord(sq[1]) - ord('1')
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

class StraDoS2Parser:
    def __init__(self, encoding: list) -> None:
        """
        page 90 of Vincent de Boer's MSc. thesis:
        http://www.kbs.twi.tudelft.nl/docs/MSc/2007/deBoer/thesis.pdf
        """
        self.pieces = {
            'R': ['M'] + [ chr(i) for i in range(ord('B') + 1, ord('M')) ] + ['B'],
            'B': ['Y'] + [ chr(i) for i in range(ord('N') + 1, ord('Y')) ] + ['N']
        }

        self.decode = {
            **{ self.pieces['R'][rank]: piece for rank, piece in enumerate(encoding) },
            **{ self.pieces['B'][rank]: piece for rank, piece in enumerate(encoding) }
        }

    def parse(self, setup: str) -> str:
        """Parse a 40-character setup string."""
        assert len(setup) == 40
        return ''.join([ self.decode[piece] for piece in setup ])

    def __call__(self, field_content: str) -> (str, str):
        """Read a 100-character field content string and return a tuple of two parsed 40-character setup strings."""
        assert len(field_content) == 100
        setup_R = self.parse(field_content[:40]      )
        setup_B = self.parse(field_content[60:][::-1])
        return setup_R, setup_B

class Pattern:
    def board2string(pat2d: str) -> str:
        return ''.join(reversed(pat2d.splitlines()))

    def any(df: pd.DataFrame, piece: str, indices: list, column: str='setup_str') -> pd.DataFrame:
        pred = lambda x: any(x[index] == piece for index in indices)
        return df.loc[lambda x: x[column].apply(pred)]

    def equal(df: pd.DataFrame, pat2d: str, column: str='setup_str') -> pd.DataFrame:
        pat = board2string(pat2d)
        return df.query(column + ' == @pat')

    def match(df: pd.DataFrame, pat2d: str, column: str='setup_str') -> pd.DataFrame:
        pat = board2string(pat2d)
        return df.query(column + '.str.match(@pat)')

def 
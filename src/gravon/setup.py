#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

class Piece:
    @staticmethod
    def names() -> list:
        """Return the list of piece names in ascending order of rank."""
        return [ 'flag', 'spy', 'scout', 'miner', 'sergeant', 'lieutenant', 'captain', 'major', 'colonel', 'general', 'marshal', 'bomb' ]

    @staticmethod
    def symbols(notation: str='EU') -> list:
        """Return a list of piece symbols in ascending order of rank."""
        return {
            'EU': [ 'F', '1' ] + [ str(rank) for rank in          range(2, 10)  ] + [ 'X', 'B' ],
            'US': [ 'F', 'S' ] + [ str(rank) for rank in reversed(range(2, 10)) ] + [ '1', 'B' ]
        }[notation]

    @staticmethod
    def ranks(notation: str='EU') -> list:
        """Return a dictionary of piece symbols and their corresponding ranks."""
        return {
            n: dict(zip(Piece.symbols(n), range(12)))
            for n in [ 'EU', 'US' ]
        }[notation]

vdb = """
6225263X26
54B1927782
4B4785B564
23B23BFB33
"""

vdbs = ''.join(reversed(vdb.splitlines()))

class Board:
    nrow, ncol = shape = (4, 10)

    row_labels = [ str(r + 1)        for r in range(nrow) ]
    col_labels = [ chr(c + ord('a')) for c in range(ncol) ]

    @staticmethod
    def to_square(loc) -> str:
        return Board.col_labels[loc[1]] + Board.row_labels[loc[0]]

    @staticmethod
    def rank_counts(game_type: str='classic') -> list:
        """Return a list of piece counts in ascending order of rank for the initial setup."""
        return {
            'classic' : [ 1, 1, 8, 5, 4, 4, 4, 3, 2, 1, 1, 6 ],
            'barrage' : [ 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1 ],
            'duel'    : [ 1, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 2 ],
            'ultimate': [ 1, 1, 4, 2, 2, 2, 2, 1, 1, 1, 1, 2 ]
        }[game_type]

    @staticmethod
    def unique_ranks(game_type: str='classic') -> list:
        """Return a list of unique piece ranks in ascending order of rank for the initial setup."""
        return {
            gt: [
                rank for rank in range(12)
                if Board.rank_counts(gt)[rank] == 1
            ]
            for gt in [ 'classic', 'barrage', 'duel', 'ultimate' ]
        }[game_type]

    lanes = [ 'L' ] * 3 + [ 'M' ] * 4 + [ 'R' ] * 3

    side_cols = [ list(range(0, 5)), list(range(5, 10)) ]
    side_char = [ 'L', 'R' ]

    def __init__(self, setup: str, notation: str='EU', game_type: str='classic') -> None:
        assert len(setup) == Board.nrow * Board.ncol
        self.matrix = np.array([
            Piece.ranks(notation)[symbol]
            for symbol in setup
        ]).reshape(Board.shape)
        self.tensor = np.array([
            self.matrix == rank
            for rank in range(12)
        ]).astype(int)
        self.game_type = game_type
        assert self.is_legal()

    def is_legal(self) -> bool:
        return dict(zip(*np.unique(self.matrix, return_counts=True))) == {
            rank: count
            for rank in range(12)
            for count in [ Board.rank_counts(self.game_type)[rank] ]
            if count > 0
        }

    def diagram(self, notation='EU', rowsep: str='\n', colsep: str=' ') -> str:
        hborder = ' ' + colsep + '+' + (Board.ncol + (Board.ncol + 1) * len(colsep)) * '-' + '+'
        vborder = '|'
        return rowsep.join(
            [ hborder ] +
            [
                colsep.join(
                    [ list(reversed(Board.row_labels))[idx] ] +
                    [ vborder ] +
                    [ Piece.symbols(notation)[rank] for rank in row ] +
                    [ vborder ]
                )
                for idx, row in enumerate(np.flip(self.matrix, axis=0))
            ] +
            [ hborder ] +
            [ (2 * ' ') + (2 * colsep) + colsep.join(Board.col_labels) ]
        )

    def argwhere(self, rank: int) -> list:
        return np.argwhere(self.tensor[rank,:,:])

    def lane(self, rank: int) -> list:
        assert symbol in Piece.symbols(notation)
        return [ 
            Board.lanes[loc] 
            for loc in np.where(self.tensor[Piece.ranks(notation)[symbol],:,:])[1] 
        ]

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
    symbols = {
        'R': ['M'] + [ chr(i) for i in range(ord('B') + 1, ord('M')) ] + ['B'],
        'B': ['Y'] + [ chr(i) for i in range(ord('N') + 1, ord('Y')) ] + ['N']
    }

    def __init__(self, encoding: list) -> None:
        """
        page 90 of Vincent de Boer's MSc. thesis:
        http://www.kbs.twi.tudelft.nl/docs/MSc/2007/deBoer/thesis.pdf
        """
        self.decode = {
            **{ StraDoS2Parser.symbols['R'][rank]: symbol for rank, symbol in enumerate(encoding) },
            **{ StraDoS2Parser.symbols['B'][rank]: symbol for rank, symbol in enumerate(encoding) }
        }

    def parse(self, setup: str) -> str:
        """Parse a 40-character setup string."""
        assert len(setup) == 40
        return ''.join([ self.decode[symbol] for symbol in setup ])

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

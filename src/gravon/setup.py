#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from typing import List, Tuple

import numpy as np
import pandas as pd

from gravon.piece import Rank, rank_labels, rank_labels_US, rank_lookup, rank_counts

def inner(padded):
    return padded[1:-1, 1:-1]

H, W = 4, 10

row_labels = [ str(row +      1  ) for row in range(H) ]
col_labels = [ chr(col + ord('a')) for col in range(W) ]

class Setup:
    matrix_init = np.full((H + 2, W + 2), Rank.lake, dtype='int8')
    matrix_init[-1, 1: 3] = Rank.empty
    matrix_init[-1, 5: 7] = Rank.empty
    matrix_init[-1, 9:11] = Rank.empty

    def __init__(self, setup_str: str, type='classic'):
        assert len(setup_str) == H * W
        self.matrix = Setup.matrix_init.copy()
        self.matrix[1:-1, 1:-1] = np.array([
            rank_lookup[r]
            for r in setup_str
        ]).reshape((H, W))
        self.tensor = np.array([
            inner(self.matrix) == r
            for r in Rank
        ], dtype='int8')
        self.type = type     

    def __str__(self) -> str:
        return Setup.to_str(self.matrix)

    def mirrored_str(self) -> str:
        return Setup.to_str(np.flip(self.matrix, axis=1))
        
    def standard_str(self) -> str:
        flag_on_left = np.argwhere(self.tensor[Rank._F])[0, 1] < (W // 2)
        return str(self) if flag_on_left else self.mirrored_str()

    def matched_str(self, match_type: str) -> str:
        return str(self) if match_type == 'identity' else self.mirrored_str()

    @staticmethod
    def to_str(matrix: np.array) -> str:
        return ''.join(
            rank_labels[r] 
            for r in inner(matrix).flatten() 
        )

    def ok(self) -> bool:
        return (
            dict(zip(*np.unique(inner(self.matrix), return_counts=True))) ==
            { 
                rank: count
                for rank, count in zip(Rank, rank_counts[self.type])
                if count > 0
            }
        )

def add_mirrored(df: pd.DataFrame) -> pd.DataFrame:
    return (df.
        assign(
            mirrored_str = lambda r: r.setup_obj.apply(lambda x: x.mirrored_str()),
            mirrored_obj = lambda r: r.apply(lambda x: Setup(x.mirrored_str, x.type), axis=1)
        )
    )

def add_standard(df: pd.DataFrame) -> pd.DataFrame:
    return (df.
        assign(
            standard_str = lambda r: r.setup_obj.apply(lambda x: x.standard_str()),
            standard_obj = lambda r: r.apply(lambda x: Setup(x.standard_str, x.type), axis=1)
        )
    )

def add_matched(df: pd.DataFrame) -> pd.DataFrame:
    return (df.
        assign(
            matched_str = lambda r: r.apply(lambda x: x.setup_obj.matched_str(x.match_type), axis=1),
            matched_obj = lambda r: r.apply(lambda x: Setup(x.matched_str, x.type), axis=1)
        )
    )

Square = Tuple[int, int]

def square_where(condition: np.array) -> Square:
    return tuple((np.argwhere(condition))[0])

def add_unique_piece(df: pd.DataFrame, rank: int) -> pd.DataFrame:
    return (df.
        assign(**{ 
            f'square_{rank_labels[rank]}': lambda r: r.setup_obj.apply(lambda x: square_where(x.matrix[1:-1,1:-1] == rank)),
            f'side_{rank_labels[rank]}'  : lambda r: r[f'square_{rank_labels[rank]}'].apply(lambda x: np.where(x[1] < (W // 2), 'left', 'right'))
        })
    )

class Theme:
    def __init__(self, rowsep='\n', colsep=' ', coordinates=True, frame=True, vborder='|', hborder='-', corner='+'):
        self.coordinates = coordinates
        self.frame = frame
        self.rowsep = rowsep
        self.colsep = colsep
        self.vborder = vborder
        self.hborder = hborder
        self.corner = corner

theme_classic = Theme()
theme_minimal = Theme(colsep='', coordinates=False, frame=False)

def diagram(setup_str: str, theme=theme_classic) -> str:
    matrix = np.array([c for c in setup_str]).reshape((H, W))
    hframe = (' ' + theme.colsep) * theme.coordinates + theme.corner + (len(theme.colsep) + (1 + len(theme.colsep)) * W) * theme.hborder + theme.corner
    return theme.rowsep.join(
        [ hframe ] * theme.frame +
        [
            theme.colsep.join(
                [ list(reversed(row_labels))[idx] ] * theme.coordinates +
                [ theme.vborder ] * theme.frame +
                [ c for c in row ] +
                [ theme.vborder ] * theme.frame
            )
            for idx, row in enumerate(np.flip(matrix, axis=0))
        ] +
        [ hframe ] * theme.frame +
        [ (2 * ' ') + (2 * theme.colsep) + theme.colsep.join(col_labels) ] * theme.coordinates
    )

# class Board:
#     nrow, ncol = shape = (4, 10)


#     @staticmethod
#     def to_square(loc) -> str:
#         return Board.col_labels[loc[1]] + Board.row_labels[loc[0]]

#     @staticmethod
#     def rank_counts(game_type: str='classic') -> list:
#         """Return a list of piece counts in ascending order of rank for the initial setup."""
#         return {
#             'classic' : [ 1, 1, 8, 5, 4, 4, 4, 3, 2, 1, 1, 6,  0, 0 ],
#             'ultimate': [ 1, 1, 4, 2, 2, 2, 2, 1, 1, 1, 1, 2, 20, 0 ],
#             'duel'    : [ 1, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 2, 30, 0 ],
#             'barrage' : [ 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1, 32, 0 ]
#         }[game_type]

#     @staticmethod
#     def unique_ranks(game_type: str='classic') -> list:
#         """Return a list of unique piece ranks in ascending order of rank for the initial setup."""
#         return {
#             gt: [
#                 rank for rank in range(12)
#                 if Board.rank_counts(gt)[rank] == 1
#             ]
#             for gt in [ 'classic', 'barrage', 'duel', 'ultimate' ]
#         }[game_type]

#     lanes = 3 * [ 'L' ] + 4 * [ 'M' ] + 3 * [ 'R' ]

#     side_cols = [ list(range(0, 5)), list(range(5, 10)) ]
#     side_char = [ 'L', 'R' ]

#     def __init__(self, placement: list, game_type: str='classic') -> None:
#         assert len(placement) == Board.nrow * Board.ncol
#         self.matrix = np.array(placement).reshape(Board.shape)
#         self.tensor = np.array([
#             self.matrix % piece.nrank == rank
#             for rank in range(piece.nrank)
#         ]).astype(int)
#         self.game_type = game_type
#         assert self.is_legal()

#     def is_legal(self) -> bool:
#         return dict(zip(*np.unique(self.matrix % piece.nrank, return_counts=True))) == {
#             rank % piece.nrank: count
#             for rank in range(piece.nrank)
#             for count in [ Board.rank_counts(self.game_type)[rank] ]
#             if count > 0
#         }

#     def __str__(self) -> str:
#         return strados2.generate(self.matrix.flatten())



    # def argwhere(self, rank: int) -> list:
    #     return np.argwhere(self.tensor[rank,:,:])

    # def lane(self, rank: int) -> list:
    #     assert symbol in Piece.symbols(notation)
    #     return [
    #         Board.lanes[loc]
    #         for loc in np.where(self.tensor[Piece.ranks(notation)[symbol],:,:])[1]
    #     ]

    # def side(self, piece: str='F') -> str:
    #     assert piece in self.unique
    #     column = self.where(piece)[1]
    #     return self.side_char[ [ column in side for side in self.side_cols ].index(True) ]

    # def mirror(self) -> Board:
    #     self.matrix = np.flip(self.matrix, axis=1)
    #     return self

    # def canonical(self, dst_side: str='L', piece: str='F') -> Board:
    #     assert piece in self.unique
    #     src_side = self.side(piece)
    #     return (self, True) if dst_side == src_side else (self.mirror(), False)

    # def square(self, sq: str) -> str:
    #     row = ord(sq[1]) - ord('1')
    #     col = ord(sq[0]) - ord('a')
    #     return self.matrix[row, col]

    # def row_sums(self, rank: int=None) -> np.array:
    #     if rank == None:
    #         return np.sum(self.tensor, axis=2)
    #     else:
    #         return np.sum(self.tensor[rank,:,:], axis=1)

    # def col_sums(self, rank: int=None) -> np.array:
    #     if rank == None:
    #         return np.sum(self.tensor, axis=1)
    #     else:
    #         return np.sum(self.tensor[rank,:,:], axis=0)

    # def lane_sums(self, rank: int=None) -> np.array:
    #     s = self.col_sums(rank)
    #     if rank == None:
    #         return np.array([ np.sum(s[:,lane], axis=1) for lane in self.lane_cols ]).transpose()
    #     else:
    #         return np.array([ np.sum(s[lane])           for lane in self.lane_cols ])

    # def side_sums(self, rank: int=None) -> np.array:
    #     s = self.col_sums(rank)
    #     if rank == None:
    #         return np.array([ np.sum(s[:,side], axis=1) for side in self.side_cols ]).transpose()
    #     else:
    #         return np.array([ np.sum(s[side])           for side in self.side_cols ])




# import gravon.pattern as pattern
# flag_a1 = (
#     """
#     ..........
#     ..........
#     ..........
#     F.........
#     """
# )
# pattern.match(df, flag_a1, mirrored=False)

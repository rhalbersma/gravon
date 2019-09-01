#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

from . import pieces
from . import strados2
from . import stratego

def setups(df: pd.DataFrame, piece_fmt: str='EU') -> pd.DataFrame:
    # parse the 100-char board string into red and blue setups
    parser = strados2.SetupParser(pieces.chars(piece_fmt))
    df['setup_tuple'] = df['field_content'].apply(lambda x: parser(x))
    df[['setup_str1', 'setup_str2']] = pd.DataFrame(df['setup_tuple'].values.tolist(), index=df.index)
    df['piece_fmt'] = piece_fmt
    df.drop(columns=['field_content', 'setup_tuple'], inplace=True)

    # tidy the wide DataFrame into long format
    df = pd.wide_to_long(df, ['name', 'setup_str'], i='game_id', j='player')
    df.reset_index(inplace=True)
    df.sort_values('game_id', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def add_WLD_score(df: pd.DataFrame) -> pd.DataFrame:
    if not all(var in df.columns for var in ['W', 'L', 'D', 'score']):
        df['W'] = df.apply(lambda x: int(x['winner'] == x['player']), axis=1)
        df['L'] = df.apply(lambda x: int(x['winner'] == 3 - x['player']), axis=1)
        df['D'] = df.apply(lambda x: int(x['winner'] == 3), axis=1)
        df['score'] = df.apply(lambda x: 1.0 * x['W'] + 0.5 * x['D'] + 0.0 * x['L'], axis=1)
    return df

def add_board(df: pd.DataFrame) -> pd.DataFrame:
    if not 'setup_board' in df.columns:
        df['setup_board'] = df.apply(lambda x: stratego.SetupBoard(x['setup_str'], x['piece_fmt'], x['game_type']), axis=1)
    return df

def add_unique_piece_locations(df: pd.DataFrame, piece_fmt: str='EU') -> pd.DataFrame:
    if not 'setup_board' in df.columns:
        df = add_board(df)
    unique_pieces = [ pieces.chars(piece_fmt)[u] for u in pieces.unique_ranks ]
    for piece in unique_pieces:
        df['lane_' + piece] = df['setup_board'].apply(lambda x: x.lane(piece))
        df['side_' + piece] = df['setup_board'].apply(lambda x: x.side(piece))
    return df

def add_unique_piece_distances(df: pd.DataFrame, piece_fmt: str='EU') -> pd.DataFrame:
    if not 'setup_board' in df.columns:
        df = add_board(df)
    manhattan = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])
    unique_pieces = [ pieces.chars(piece_fmt)[u] for u in pieces.unique_ranks ]
    for i, piece in enumerate(unique_pieces):
        for j, other in enumerate(unique_pieces):
            if i < j:
                df['dist_' + piece + other] = df['setup_board'].apply(lambda x: manhattan(x.where(piece), x.where(other)))
    return df

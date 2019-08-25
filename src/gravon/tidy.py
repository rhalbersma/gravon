#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

from . import strados2
from . import stratego

def setups(df: pd.DataFrame) -> pd.DataFrame:
    # parse the 100-char board string into red and blue setups
    parser = strados2.SetupParser(stratego.Setup.pieces)
    df['setups'] = df['field_content'].apply(lambda x: parser(x))
    df[['setup1', 'setup2']] = pd.DataFrame(df['setups'].values.tolist(), index=df.index)
    df.drop(columns=['field_content', 'setups'], inplace=True)

    # tidy the wide DataFrame into long format
    df = pd.wide_to_long(df, ['name', 'setup'], i='game_id', j='player')
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
    if not 'board' in df.columns:
        df['board'] = df.apply(lambda x: stratego.Setup(x['setup'], x['game_type']), axis=1)
    return df

unique_pieces = [ 'F', '1', '9', 'X' ]

def add_unique_piece_sides(df: pd.DataFrame) -> pd.DataFrame:
    if not 'board' in df.columns:
        df = add_board(df)
    for piece in unique_pieces:
        df['side_'  + piece] = df['board'].apply(lambda x: x.side(piece))
    return df

def add_unique_piece_distances(df: pd.DataFrame) -> pd.DataFrame:
    if not 'board' in df.columns:
        df = add_board(df)
    manhattan = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])
    for i, piece in enumerate(unique_pieces):
        for j, other in enumerate(unique_pieces):
            if i < j:
                df['dist_' + piece + other] = df['board'].apply(lambda x: manhattan(x.where(piece), x.where(other)))
    return df

#!/usr/bin/env python3

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

import strados2
import stratego

def setups(df: pd.DataFrame) -> pd.DataFrame:
    parser = strados2.SetupParser(stratego.Setup.pieces)
    df['setups'] = df['field_content'].apply(lambda x: parser(x))
    df[['setup1', 'setup2']] = pd.DataFrame(df['setups'].values.tolist(), index=df.index)
    df.drop(columns=['field_content', 'setups'], inplace=True)

    df = pd.wide_to_long(df, ['name', 'setup'], i='game_id', j='player')
    df.reset_index(inplace=True)
    df.sort_values('game_id', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['array'] = df.apply(lambda x: stratego.Setup(x['setup'], x['game_type']), axis=1)

    unique_pieces = [ 'F', '1', '9', 'X' ]
    for piece in unique_pieces:
        df['where_' + piece] = df['array'].apply(lambda x: x.where(piece))
        df['side_'  + piece] = df['array'].apply(lambda x: x.side(piece))

    dist = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])
    for piece in unique_pieces:
        for other in unique_pieces:
            if piece != other:
                df['dist_' + piece + other] = df.apply(lambda x: dist(x['where_' + piece], x['where_' + other]), axis=1)

    df['W'] = df.apply(lambda x: int(x['winner'] == x['player']), axis=1)
    df['L'] = df.apply(lambda x: int(x['winner'] == 3 - x['player']), axis=1)
    df['D'] = df.apply(lambda x: int(x['winner'] == 3), axis=1)
    df['G'] = 1
    df['score'] = df.apply(lambda x: 0.5 if x['winner'] == 3 else float(x['winner'] == x['player']), axis=1)

    return df

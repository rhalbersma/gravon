#!/usr/bin/env python3

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

import strados2
import stratego

parser = strados2.SetupParser(stratego.Setup.pieces)

def setups_from_games(filepath_or_buffer) -> pd.DataFrame:
    games = pd.read_csv(filepath_or_buffer)
    games['setup1'] = games.apply(lambda x: stratego.Setup(parser(x['field_content'][:40], 'R'), x['game_type']), axis=1)
    games['setup2'] = games.apply(lambda x: stratego.Setup(parser(x['field_content'][60:], 'B'), x['game_type']), axis=1)
    games.drop(columns=['field_content'], inplace=True)
    setups = pd.wide_to_long(games, ['name', 'setup'], i='game_id', j='player')
    setups.reset_index(inplace=True)

    unique_pieces = [ 'F', '1', '9', 'X' ]
    for piece in unique_pieces:
        setups['side_' + piece] = setups['setup'].apply(lambda x: x.side(piece))
    setups['string'] = setups['setup'].apply(lambda x: str(x))

    setups['W'] = setups.apply(lambda x: int(x['winner'] == x['player']), axis=1)
    setups['L'] = setups.apply(lambda x: int(x['winner'] == 3 - x['player']), axis=1)
    setups['D'] = setups.apply(lambda x: int(x['winner'] == 3), axis=1)
    setups['score'] = setups.apply(lambda x: 0.5 if x['winner'] == 3 else float(x['winner'] == x['player']), axis=1)

    return setups

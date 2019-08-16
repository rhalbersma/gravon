#!/usr/bin/env python3

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

import strados2
import stratego

def validate(x: str):
    return stratego.Setup(strados2.Decode()(x))

def setups_from_games(filepath_or_buffer):
    games = pd.read_csv(filepath_or_buffer)
    games = (games
    .assign(setup1 = games['field_content'].apply(lambda x: validate(x[:40]      )))
    .assign(setup2 = games['field_content'].apply(lambda x: validate(x[60:][::-1])))
    )
    games.drop(columns=['field_content'], inplace=True)
    setups = pd.wide_to_long(games, ['name', 'setup'], i='game_id', j='player')
    setups.reset_index(inplace=True)

    setups = (setups
    .assign(side_F = setups['setup'].apply(lambda x: x.side('F')))
    .assign(side_X = setups['setup'].apply(lambda x: x.side('X')))
    .assign(side_9 = setups['setup'].apply(lambda x: x.side('9')))
    .assign(side_1 = setups['setup'].apply(lambda x: x.side('1')))
    )
    setups['strados2'] = setups['setup'].apply(lambda x: x.strados2())

    setups['W'] = setups.apply(lambda x: int(x['winner'] == x['player']), axis=1)
    setups['L'] = setups.apply(lambda x: int(x['winner'] == 3 - x['player']), axis=1)
    setups['D'] = setups.apply(lambda x: int(x['winner'] == 3), axis=1)
    setups['score'] = setups.apply(lambda x: 0.5 if x['winner'] == 3 else float(x['winner'] == x['player']), axis=1)

    return setups

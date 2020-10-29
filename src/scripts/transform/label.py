#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from typing import Tuple

import pandas as pd

_type = {
    0: 'classic',
    1: 'barrage',
    2: 'free',
    3: 'ultimate',
    4: 'duel'
}

_player = {
    0: 'red',
    1: 'blue'
}

_winner = {
    0: 'red',
    1: 'blue',
    2: 'draw'
}

_ending = {
     0: 'unable to move',
     1: 'flag captured',
     2: 'both unable to move',
     3: 'forfeit',
     4: 'tie agreed',
    10: 'both missing',
    11: 'player clock timed out',
    12: 'game clock timed out',
    13: 'player clock timed out (and player was missing)',
    14: 'opponent missing'
}

_num_turns = {
    0: '<50',
    1:  '50-100',
    2: '100-150',
    3: '150-200',
    4: '200-250',
    5: '250-300',
    6: '300-350',
    7: '>350'
}

def txt_files(parsed: pd.DataFrame) -> pd.DataFrame:
    return (parsed
        .replace({
            'type': _type
        })
        .astype(dtype={
            'gid'          : 'int32',
            'url'          : 'category',
            'name'         : 'category',
            'last_modified': pd.CategoricalDtype(ordered=True),
            'modified'     : pd.CategoricalDtype(ordered=True),
            # filename     : object
            'prefix'       : 'category',
            # period       : object
            'freq'         : 'category',
            'no'           : 'int32',
            'ext'          : 'category',
            'type'         : pd.CategoricalDtype(categories=_type.values())
        })
        .loc[:,[
            'gid', 'url', 'name', 'last_modified', 'modified', 'filename', 'prefix', 'period', 'freq', 'no', 'ext', 'type'
        ]]
    )

def index(parsed: pd.DataFrame) -> pd.DataFrame:
    return (parsed
        .assign(
            num_turns = lambda r: r.num_moves.apply(lambda n: min(n // 100, 7)),
            next_move = lambda r: r.num_moves % 2
        )
        .replace({
            'type'     : _type,
            'winner'   : _winner,
            'ending'   : _ending,
            'num_turns': _num_turns,
            'next_move': _player
        })
        .astype(dtype={
            'gid'          : 'int32',
            'type'         : pd.CategoricalDtype(categories=_type.values()),
            'player_red'   : 'category',
            'player_blue'  : 'category',
            'winner'       : pd.CategoricalDtype(categories=_winner.values()),
            'ending'       : pd.CategoricalDtype(categories=_ending.values()),
            'num_moves'    : 'int16',
            'num_turns'    : pd.CategoricalDtype(categories=_num_turns.values()),
            'next_move'    : pd.CategoricalDtype(categories=_player.values())
            # field_content: object
        })
        .loc[:,[
            'gid', 'type', 'player_red', 'player_blue', 'winner', 'ending', 'num_moves', 'num_turns', 'next_move', 'field_content'
        ]]
    )

def games(parsed: pd.DataFrame) -> pd.DataFrame:
    return (parsed
        .astype(dtype={
            'gid'   : 'int32',
            'mid'   : 'int16',
            'source': 'category',
            'target': 'category'
        })
    )

def index_games(parsed: Tuple[pd.DataFrame, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return index(parsed[0]), games(parsed[1])

def setups(parsed: pd.DataFrame) -> pd.DataFrame:
    return (parsed
        .astype(dtype={
            'player': pd.CategoricalDtype(categories=_player.values())
        })
    )

def results(parsed: pd.DataFrame) -> pd.DataFrame:
    return (parsed
        .pipe(lambda x: x.set_axis(x
            .columns
            .str.lower()
            .str.replace(' ', '_')
            , axis='columns'
        ))
        .reset_index()
        .rename(columns = {
            'index'     : 'rid',
            '#_of_turns': 'num_turns'
        })
        .replace({'type': {
            'Classic'           : 0,
            'Barrage'           : 1,
            'Free'              : 2,
            'Ultimate Lightning': 3,
            'Duell'             : 4
        }})
        .replace({'type': _type})
        .astype(dtype={
            'type'     : pd.CategoricalDtype(categories=_type.values()),
            'ending'   : pd.CategoricalDtype(categories=_ending.values()),
            'num_turns': pd.CategoricalDtype(categories=_num_turns.values())
        })
        .loc[:, [
            'rid', 'date', 'time', 'type', 'player_red', 'player_blue', 'result', 'ending', 'num_turns', 'duration'
        ]]
    )

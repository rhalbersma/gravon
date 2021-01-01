#          Copyright Rein Halbersma 2018-2021.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from typing import Tuple

import numpy as np
import pandas as pd

import gravon.package as pkg
from gravon.piece import Rank
from gravon.setup import Setup
import gravon.strados2 as strados2

import scripts.transform.games as games
import scripts.transform.label as label


def get_setups() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        db_setups   = pkg.load_dataset(  'db_setups')
        game_setups = pkg.load_dataset('game_setups')
        free_setups = pkg.load_dataset('free_setups')
        null_setups = pkg.load_dataset('null_setups')
    except:
        st2 = games.get_st2()
        si2, _ = games.get_si2_sg2()
        free_setups = si2.query('type == "free"')
        null_setups = si2.query('field_content.isnull()')
        game_setups = (si2
            .query('type != "free" & field_content.notnull()')
            .assign(
                setup_str_red  = lambda r: r.field_content.str[:40],
                setup_str_blue = lambda r: r.field_content.str[60:].str[::-1],
                dmz            = lambda r: r.field_content.str[40:60]
            )
        )
        assert (game_setups.dmz == 'AA__AA__AAAA__AA__AA').all()
        db_setups = (pd
            .wide_to_long(
                st2.merge(game_setups).drop(columns=['player_red', 'player_blue', 'dmz']), 
                stubnames=['setup_str'], i='gid', j='player', sep='_', suffix='(red|blue)'
            )
            .reset_index()
            .assign(
                result    = lambda r: np.where(r.player == r.winner, 'win', np.where(r.winner == 'draw', 'draw', 'loss')),
                score     = lambda r: np.where(r.result == 'win', 1.0, np.where(r.result == 'draw', 0.5, 0.0)),
                setup_str = lambda r: r.setup_str.apply(strados2.decode_setup),
                setup_obj = lambda r: r.apply(lambda x: Setup(x.setup_str, x.type), axis=1)
            )
            .astype(dtype={
                'result': pd.CategoricalDtype(categories=['win', 'draw', 'loss'])
            })
            .pipe(lambda df: pd.concat([df, pd.get_dummies(df.result, prefix='', prefix_sep='')], axis=1))            
            .loc[:, [
                'gid', 'filename', 'period', 'freq', 'ext', 'type', 'player', 
                'result', 'win', 'draw', 'loss', 'score', 'ending', 
                'num_moves', 'num_turns', 'next_move', 
                'setup_str', 'setup_obj'
            ]]
            .pipe(label.setups)
            .sort_values(['gid', 'player'])
            .reset_index(drop=True)
        )
        assert all(db_setups.setup_obj.apply(lambda x: x.ok()))
        pkg.save_dataset(  db_setups,   'db_setups')
        pkg.save_dataset(game_setups, 'game_setups')
        pkg.save_dataset(free_setups, 'free_setups')
        pkg.save_dataset(null_setups, 'null_setups')
    return db_setups, game_setups, free_setups, null_setups


def print_setup_summary():
    st2 = games.get_st2()
    _, game_setups, free_setups, null_setups = get_setups()
    print(pd.pivot_table(st2.merge(game_setups), index=['freq', 'ext', 'player_red', 'player_blue'], columns=['type'], aggfunc='size', fill_value=0, observed=True), '\n')
    print(pd.pivot_table(st2.merge(free_setups), index=['freq', 'ext', 'player_red', 'player_blue'], columns=['type'], aggfunc='size', fill_value=0, observed=True), '\n')
    print(pd.pivot_table(st2.merge(null_setups), index=['freq', 'ext', 'player_red', 'player_blue'], columns=['type'], aggfunc='size', fill_value=0, observed=True), '\n')


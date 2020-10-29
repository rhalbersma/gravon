#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from typing import Tuple

import numpy as np
import pandas as pd

import gravon.package as pkg
from gravon.setup import Setup
import gravon.strados2 as strados2

import scripts.transform.games as games
import scripts.transform.label as label

def get_ss2() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        ss2 = pkg.load_dataset('ss2')
        game_setup = pkg.load_dataset('game_setup')
        free_setup = pkg.load_dataset('free_setup')
        null_setup = pkg.load_dataset('null_setup')
    except:
        st2 = games.get_st2()
        si2, _ = games.get_si2_sg2()
        free_setup = si2.query('type == "free"')
        null_setup = si2.query('field_content.isnull()')
        game_setup = (si2
            .query('type != "free" & field_content.notnull()')
            .assign(
                setup_str_red  = lambda r: r.field_content.str[:40],
                setup_str_blue = lambda r: r.field_content.str[60:].str[::-1],
                dmz            = lambda r: r.field_content.str[40:60]
            )
        )
        assert (game_setup.dmz == 'AA__AA__AAAA__AA__AA').all()
        ss2 = (pd
            .wide_to_long(
                st2.merge(game_setup).drop(columns=['player_red', 'player_blue', 'dmz']), 
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
                'num_moves', 'num_turns', 'next_move', 'setup_str', 'setup_obj'
            ]]
            .pipe(label.setups)
            .sort_values(['gid', 'player'])
            .reset_index(drop=True)
        )
        assert all(ss2.setup_obj.apply(lambda x: x.ok()))
        pkg.save_dataset(ss2, 'ss2')
        pkg.save_dataset(game_setup, 'game_setup')
        pkg.save_dataset(free_setup, 'free_setup')
        pkg.save_dataset(null_setup, 'null_setup')
    return ss2, game_setup, free_setup, null_setup

def print_setup_summary():
    st2 = games.get_st2()
    _, game_setup, free_setup, null_setup = get_ss2()
    print(pd.pivot_table(st2.merge(game_setup), index=['freq', 'ext', 'player_red', 'player_blue'], columns=['type'], aggfunc='size', fill_value=0, observed=True), '\n')
    print(pd.pivot_table(st2.merge(free_setup), index=['freq', 'ext', 'player_red', 'player_blue'], columns=['type'], aggfunc='size', fill_value=0, observed=True), '\n')
    print(pd.pivot_table(st2.merge(null_setup), index=['freq', 'ext', 'player_red', 'player_blue'], columns=['type'], aggfunc='size', fill_value=0, observed=True), '\n')

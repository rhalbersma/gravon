#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from typing import Tuple

import numpy as np
import pandas as pd

import gravon.package as pkg
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
                setup_red  = lambda r: r.field_content.str[:40],
                setup_blue = lambda r: r.field_content.str[60:].str[::-1],
                dmz        = lambda r: r.field_content.str[40:60]
            )
        )
        assert (game_setup.dmz == 'AA__AA__AAAA__AA__AA').all()
        ss2 = (pd
            .wide_to_long(
                st2.merge(game_setup).drop(columns=['player_red', 'player_blue', 'dmz']), 
                stubnames=['setup'], i='gid', j='player', sep='_', suffix='(red|blue)'
            )
            .reset_index()
            .assign(
                result = lambda r: np.where(r.player == r.result, 1.0, np.where(r.result == "draw", 0.5, 0.0)),
                setup  = lambda r: r.setup.apply(strados2.decode_setup)
            )
            .loc[:, [
                'gid', 'filename', 'period', 'freq', 'ext', 'type', 'player', 'result', 'ending', 'num_moves', 'num_turns', 'next_move', 'setup'
            ]]
            .pipe(label.setups)
            .sort_values(['gid', 'player'])
            .reset_index(drop=True)
        )
        pkg.save_dataset(ss2, 'ss2')
        pkg.save_dataset(game_setup, 'game_setup')
        pkg.save_dataset(free_setup, 'free_setup')
        pkg.save_dataset(null_setup, 'null_setup')
    return ss2, game_setup, free_setup, null_setup

def print_setup_summary():
    st2 = games.get_st2()
    _, game_setup, free_setup, null_setup = get_ss2()
    print(st2.merge(game_setup).groupby(['freq', 'ext', 'player_red', 'player_blue', 'type'], observed=True).size().unstack(fill_value=0), '\n')
    print(st2.merge(free_setup).groupby(['freq', 'ext', 'player_red', 'player_blue', 'type'], observed=True).size().unstack(fill_value=0), '\n')
    print(st2.merge(null_setup).groupby(['freq', 'ext', 'player_red', 'player_blue', 'type'], observed=True).size().unstack(fill_value=0), '\n')


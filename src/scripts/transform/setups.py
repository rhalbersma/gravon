#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

import gravon.package         as pkg
import gravon.transform.label as label

si2 = pkg.load_dataset('si2')
regular_games = (si2
    .query('type != "free" & field_content.notnull()')
    .assign(
        setup_red  = lambda r: r.field_content.str[:40],
        setup_blue = lambda r: r.field_content.str[60:].str[::-1],
        dmz        = lambda r: r.field_content.str[40:60]
    )
    .loc[:, [
        'gid', 'filename', 'period', 'freq', 'ext', 'type', 'player_red', 'player_blue', 'result', 'ending', 'num_moves', 'num_turns', 'next_move', 'setup_red', 'setup_blue', 'dmz'
    ]]
)

assert regular_games.groupby(['freq', 'ext', 'player_red', 'player_blue', 'type'], observed=True).size().unstack(fill_value=0).shape[0] == 2
dmz = 'AA__AA__AAAA__AA__AA'
assert (regular_games.dmz == dmz).all()

ss2 = (pd
    .wide_to_long(
        regular_games.drop(columns=['player_red', 'player_blue', 'dmz']), 
        stubnames=['setup'], i='gid', j='player', sep='_', suffix='(red|blue)'
    )
    .reset_index()
    .loc[:, [
        'gid', 'player', 'filename', 'period', 'freq', 'ext', 'type', 'result', 'ending', 'num_moves', 'num_turns', 'next_move', 'setup'
    ]]
    .pipe(label.setups)
    .sort_values(['gid', 'player'])
    .reset_index(drop=True)
)
pkg.save_dataset(ss2, 'ss2')

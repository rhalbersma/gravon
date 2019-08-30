#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

from gravon import tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
piece_fmt = 'EU'
setups = tidy.setups(games.copy(), piece_fmt)

# http://forum.stratego.com/topic/2429-analyzing-game-setups/?p=38121
setups = tidy.add_unique_piece_sides(setups, piece_fmt)
piece, other = pieces.chars[piece_fmt][0], pieces.chars[piece_fmt][10]
print('{} and {} starting on the same side:\n'.format(piece, other))
print('{}\n'.format(pd.value_counts(setups['side_' + piece] == setups['side_' + other], normalize=True, sort=False)))

# Unpublished analysis
print('{}\n'.format((setups['side_' + piece] == 'R').corr(setups['side_' + other] == 'R')))
print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='all')))
print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='index')))
print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='columns')))

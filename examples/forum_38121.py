#          Copyright Rein Halbersma 2018-2021.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/2429-analyzing-game-setups/?p=38121

import pandas as pd

from gravon import pieces, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_unique_piece_locations(setups, piece_fmt)

piece, other = pieces.chars()[0], pieces.chars()[10]
print('{} and {} starting on the same side:\n'.format(piece, other))
print('{}\n'.format(pd.value_counts(setups['side_' + piece] == setups['side_' + other], normalize=True, sort=False)))

# Unpublished analysis
print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='all')))
print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='index')))
print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='columns')))

print('{} and {} starting in the same lane:\n'.format(piece, other))
print('{}\n'.format(pd.value_counts(setups['lane_' + piece] == setups['lane_' + other], normalize=True, sort=False)))

print('{}\n'.format(pd.crosstab(setups['lane_' + piece], setups['lane_' + other], margins=True, normalize='all')))
print('{}\n'.format(pd.crosstab(setups['lane_' + piece], setups['lane_' + other], margins=True, normalize='index')))
print('{}\n'.format(pd.crosstab(setups['lane_' + piece], setups['lane_' + other], margins=True, normalize='columns')))

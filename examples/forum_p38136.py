#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

from gravon import pieces, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://forum.stratego.com/topic/2429-analyzing-game-setups/?p=38136
setups = tidy.add_unique_piece_sides(setups)

unique_pieces = [ pieces.chars['EU'][u] for u in pieces.unique_ranks ]
for i, piece in enumerate(unique_pieces):
    for j, other in enumerate(unique_pieces):
        if i < j:
            print('{} and {} starting on the same side:\n'.format(piece, other))
            print('{}\n'.format(pd.value_counts(setups['side_' + piece] == setups['side_' + other], normalize=True, sort=False)))

            # Unpublished analysis
            print('{}\n'.format(pd.Series(setups['side_' + piece] == 'R').corr(setups['side_' + other] == 'R')))
            print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='all')))
            print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='index')))
            print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='columns')))

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

from gravon import tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66725
setups = tidy.add_unique_piece_distances(setups)

for i, piece in enumerate(tidy.unique_pieces):
    for j, other in enumerate(tidy.unique_pieces):
        if i < j:
            print('Distance between {} and {} in the starting setup: {}'.format(piece, other, setups['dist_' + piece + other].agg('mean')))

# Unpublished analysis
setups = tidy.add_WLD_score(setups)

for i, piece in enumerate(tidy.unique_pieces):
    for j, other in enumerate(tidy.unique_pieces):
        if i < j:
            print('{}\n'.format(setups.groupby('dist_' + piece + other).agg(['count', 'mean'])['score']))

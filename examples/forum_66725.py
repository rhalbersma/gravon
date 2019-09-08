#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66725

import pandas as pd

from gravon import pieces, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_unique_piece_distances(setups)
setups = tidy.add_WLD_score(setups)

unique_pieces = [ pieces.chars()[u] for u in pieces.unique_ranks() ]

for i, piece in enumerate(unique_pieces):
    for j, other in enumerate(unique_pieces):
        if i < j:
            print('Distance between {} and {} in the starting setup: {}'.format(piece, other, setups['dist_' + piece + other].agg('mean')))

for i, piece in enumerate(unique_pieces):
    for j, other in enumerate(unique_pieces):
        if i < j:
            print('{}\n'.format(setups.groupby('dist_' + piece + other).agg(['count', 'mean'])['score']))

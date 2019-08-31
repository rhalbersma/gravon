#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

from gravon import stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
piece_fmt = 'EU'
setups = tidy.setups(games.copy(), piece_fmt)
piece_chars = pieces.chars[piece_fmt]
piece_ranks = pieces.ranks[piece_fmt]

# http://stratego-tips.blogspot.com/2017/04/common-stratego-piece-placements.html
setups = tidy.add_board(setups)
count, probs = setups['setup_board'].apply(lambda x: x.tensor).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:5.3f}'.format}, linewidth=100)

print('Placement by piece and square')
for piece in piece_chars:
    r = piece_ranks[piece]
    print('{}'.format(piece))
    print('{}\n'.format(np.flip(probs[r,:,:], axis=1)))

print('Placement by piece and column')
for piece in piece_chars:
    r = piece_ranks[piece]
    print('{}: {}'.format(piece, np.sum(probs[r,:,:], axis=0)))
print()

print('Placement by piece and row')
for piece in piece_chars:
    r = piece_ranks[piece]
    print('{}: {}'.format(piece, np.sum(probs[r,:,:], axis=1)))
print()

np.set_printoptions()

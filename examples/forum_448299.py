#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=448299

import numpy as np
import pandas as pd

from gravon import pieces, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_board(setups)

count, probs = setups['board'].apply(lambda x: x.tensor).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:5.3f}'.format}, linewidth=100)

print('Placement by piece and square')
for piece in pieces.chars():
    r = pieces.ranks()[piece]
    print('{}'.format(piece))
    print('{}\n'.format(np.flip(probs[r,:,:], axis=1)))

print('Placement by piece and column')
for piece in pieces.chars():
    r = pieces.ranks()[piece]
    print('{}: {}'.format(piece, np.sum(probs[r,:,:], axis=0)))
print()

print('Placement by piece and row')
for piece in pieces.chars():
    r = pieces.ranks()[piece]
    print('{}: {}'.format(piece, np.sum(probs[r,:,:], axis=1)))
print()

np.set_printoptions()

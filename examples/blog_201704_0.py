#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

from gravon import pieces, stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://stratego-tips.blogspot.com/2017/04/common-stratego-piece-placements.html
setups = tidy.add_board(setups)
count, probs = pd.Series(setups['board']).apply(lambda x: x.tensor).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:7.2%}'.format}, linewidth=100)
print('The charts below show Stratego piece placements from {:,} setups.'.format(len(setups)))
for piece in list(reversed(pieces.encoding['EU'][1:11])) + [ 'B', 'F' ]:
    r = pieces.ranks['EU'][piece]
    print('Common Stratego {} Placement\n'.format(pieces.full_names[r].capitalize()))
    print('{}\n'.format(np.flip(count[r,:,:], axis=1)))
    print('{}\n'.format(np.sum (count[r,:,:], axis=1)))
    print('{}\n'.format(np.flip(probs[r,:,:], axis=1)))
    print('{}\n'.format(np.sum (probs[r,:,:], axis=1) / stratego.Setup.counts['classic'][r]))
np.set_printoptions()

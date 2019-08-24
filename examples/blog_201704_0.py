#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

from gravon import stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://stratego-tips.blogspot.com/2017/04/common-stratego-piece-placements.html
setups = tidy.add_state(setups)
count, probs = pd.Series(setups['state']).apply(lambda x: x.placement).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:7.2%}'.format}, linewidth=100)
print('The charts below show Stratego piece placements from {:,} setups.'.format(len(setups)))
for piece in list(reversed(stratego.Setup.pieces[1:11])) + [ 'B', 'F' ]:
    r = stratego.Setup.ranks[piece]
    print('Common Stratego {} Placement\n'.format(stratego.Setup.names[r].capitalize()))
    print('{}\n'.format(np.flip(count[r,:,:], axis=1)))
    print('{}\n'.format(np.sum (count[r,:,:], axis=1)))
    print('{}\n'.format(np.flip(probs[r,:,:], axis=1)))
    print('{}\n'.format((np.sum (probs[r,:,:], axis=1) / stratego.Setup.counts['classic'][r])))
np.set_printoptions()

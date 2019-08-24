#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

from gravon import stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://forum.stratego.com/topic/2429-analyzing-game-setups/?p=34051
setups = setups.drop_duplicates(subset='setup')
setups = tidy.add_state(setups)
count, probs = pd.Series(setups['state']).apply(lambda x: x.placement).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:7.2%}'.format}, linewidth=100)
piece_order = [ 'F' ] + list(reversed(stratego.Setup.pieces[1:11])) + [ 'B' ]
rank_order = [ stratego.Setup.ranks[piece] for piece in piece_order ]
for row in reversed(range(4)):
    for col in range(10):
        print('{}{}:\n'.format(chr(col + ord('a')), row + 1))
        print('{}\n'.format(count[rank_order,row, col]))
        print('{}\n'.format(probs[rank_order,row, col]))
np.set_printoptions()

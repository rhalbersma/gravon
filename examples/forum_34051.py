#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/2429-analyzing-game-setups/?p=34051

import numpy as np
import pandas as pd

from gravon import tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = setups.drop_duplicates(subset='setup_str')
setups = tidy.add_board(setups)

count, probs = setups['board'].apply(lambda x: x.tensor).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:7.2%}'.format}, linewidth=100)

rank_order = [ 0 ] + list(reversed(range(1, 11))) + [ 11 ]
for row in reversed(range(4)):
    for col in range(10):
        print('{}{}:\n'.format(chr(col + ord('a')), row + 1))
        print('{}\n'.format(count[rank_order, row, col]))
        print('{}\n'.format(probs[rank_order, row, col]))
print('Number of Unique Stratego setups analyzed: {}'.format(len(setups)))

np.set_printoptions()

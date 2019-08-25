#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

from gravon import stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66753
setups = tidy.add_board(setups)
count, probs = pd.Series(setups['board']).apply(lambda x: x.tensor).agg(['sum', 'mean'])

unique_pieces = [ 'X', '9', '1', 'F' ]
unique_ranks = [ stratego.Setup.ranks[piece] for piece in unique_pieces ]
np.set_printoptions(formatter={'float': '{:4.3f}'.format}, linewidth=100)
print('{}\n'.format(np.sum(count[unique_ranks,:,:], axis=2)))
print('{}\n'.format(np.sum(probs[unique_ranks,:,:], axis=2)))
np.set_printoptions()

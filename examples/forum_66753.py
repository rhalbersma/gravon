#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66753

import numpy as np
import pandas as pd

from gravon import pieces, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_board(setups)

count, probs = setups['board'].apply(lambda x: x.tensor).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:4.3f}'.format}, linewidth=100)

print('{}\n'.format(np.sum(count[pieces.unique_ranks(),:,:], axis=2)))
print('{}\n'.format(np.sum(probs[pieces.unique_ranks(),:,:], axis=2)))

np.set_printoptions()

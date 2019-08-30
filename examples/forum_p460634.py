#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

from gravon import pieces, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://forum.stratego.com/topic/358733-predictability-and-bluff/?p=460634
setups = tidy.add_board(setups)
setups = tidy.add_WLD_score(setups)

# Unpublished analysis
rank_8 = 8
setups['side_balanced_colonels'] = setups['setup_board'].apply(lambda x: sum(np.sum(x.tensor[rank_8,:,:], axis=0)[:5]) == 1)
print('{}\n'.format(setups['side_balanced_colonels'].value_counts(normalize=True, sort=False)))
print('{}\n'.format(setups.groupby('side_balanced_colonels')['W', 'L', 'D', 'score'].agg(['mean'])))

rank_7 = 7
setups['row_balanced_majors'] = setups['setup_board'].apply(lambda x: max(np.sum(x.tensor[rank_7,:,:], axis=1)) == 1)
print('{}\n'.format(setups['row_balanced_majors'].value_counts(normalize=True, sort=False)))
print('{}\n'.format(setups.groupby('row_balanced_majors')['W', 'L', 'D', 'score'].agg(['mean'])))

setups['col_sum_majors'] = setups['setup_board'].apply(lambda x: np.sum(x.tensor[rank_7,:,:], axis=0))
setups['lane_balanced_majors'] = setups['col_sum_majors'].apply(lambda x: sum(x[0:3]) == sum(x[3:7]) == sum(x[7:10]))
print('{}\n'.format(setups['lane_balanced_majors'].value_counts(normalize=True, sort=False)))
print('{}\n'.format(setups.groupby('lane_balanced_majors')['W', 'L', 'D', 'score'].agg(['mean'])))

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/357414-vertical-double-bombs/?p=432201

import numpy as np
import pandas as pd

from gravon import archive, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_board(setups)
setups = tidy.add_WLD_score(setups)

rank_B = 11
setups['bombed_off_column'] = setups['board'].apply(lambda x: np.sum(x.tensor[rank_B,:,:], axis=0).max() == 4)
df = setups.query('bombed_off_column == True')
df['G'] = 1
print('{}\n'.format(df[['G', 'W', 'L', 'D']].agg(['sum'])))
print('{}\n'.format('\n'.join(df.query('W == True')['game_id'].tolist())))
print('{}\n'.format('\n'.join(df.query('D == True')['game_id'].tolist())))

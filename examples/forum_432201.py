#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://stratego-tips.blogspot.com/2017/04/top-row-open-flag-winning-game-files-at.html

import numpy as np
import pandas as pd

from gravon import archive, pattern, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_board(setups)
setups = tidy.add_WLD_score(setups)

rank_B = 11
setups['bombed_off_column'] = setups['setup_board'].apply(lambda x: max(np.sum(x.tensor[rank_B,:,:], axis=0)) == 4)
df = setups.query('bombed_off_column == True')
df['G'] = 1
print('{}\n'.format(df[['G', 'W', 'L', 'D']].agg(['sum'])))
print('{}\n'.format(df.query('W == True')['game_id']))
print('{}\n'.format(df.query('D == True')['game_id']))

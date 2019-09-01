#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/360085-data-science-tools-for-the-gravon-archive-of-stratego-games/?p=481081

import pandas as pd

from gravon import pieces, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_board(setups)
setups = tidy.add_WLD_score(setups)

colonel = pieces.names.index('colonel')

setups['side_balanced_colonels'] = setups['setup_board'].apply(lambda x: x.side_sums(colonel).max() == 1)
print('{}\n'.format(setups['side_balanced_colonels'].value_counts(normalize=True, sort=False)))
print('{}\n'.format(setups.groupby('side_balanced_colonels')['score'].agg(['count', 'mean'])))

major = pieces.names.index('major')

setups['lane_balanced_majors'] = setups['setup_board'].apply(lambda x: x.lane_sums(major).max() == 1)
print('{}\n'.format(setups['lane_balanced_majors'].value_counts(normalize=True, sort=False)))
print('{}\n'.format(setups.groupby('lane_balanced_majors')['score'].agg(['count', 'mean'])))

setups['row_balanced_majors'] = setups['setup_board'].apply(lambda x: x.row_sums(major).max() == 1)
print('{}\n'.format(setups['row_balanced_majors'].value_counts(normalize=True, sort=False)))
print('{}\n'.format(setups.groupby('row_balanced_majors')['score'].agg(['count', 'mean'])))

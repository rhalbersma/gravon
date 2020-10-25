#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66589

import pandas as pd

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')

print('{}\n'.format(games['winner'].value_counts(sort=False)))
print('{}\n'.format(games['winner'].value_counts(sort=False, normalize=True)))

# Unpublished analysis
qs = [.01, .05, .10, .25, .50, .75, .90, .95, .99]
print('{}\n'.format(games['game_length'].describe(percentiles=qs)))
print('{}\n'.format(games.groupby(by=['winner'])['game_length'].describe(percentiles=qs)))

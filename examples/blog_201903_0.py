#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

from gravon import stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://stratego-tips.blogspot.com/2019/03/listing-of-most-popular-stratego-game.html
setups = tidy.add_WLD_score(setups)

df = setups.groupby('setup').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']
})
df.reset_index(inplace=True)
df.columns = ['_'.join(col) for col in df.columns.values]
df.columns = df.columns.str.rstrip('_')
df.columns = df.columns.str.replace(r'_sum$', '')
df.columns = df.columns.str.replace(r'^score_', '')
atleast10 = df.query('count >= 10').sort_values(by=['count'], ascending=False)
atleast10.reset_index(drop=True, inplace=True)

for t in atleast10.itertuples():
    print('{}\n'.format(stratego.Setup(t.setup).diagram()))
    print('Wins = {} Losses = {} Ties = {} Games Played = {} Winning Percentage = {:5.2%}\n'.format(t.W, t.L, t.D, t.count, t.W / (t.W + t.L)))

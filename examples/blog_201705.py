#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://stratego-tips.blogspot.com/2017/05/best-winning-percentage-stratego-game.html

import pandas as pd

from gravon import archive, pattern, stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_WLD_score(setups)

df = setups.groupby('setup_str').agg({
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
best_winning_percentage = atleast10.query('count >= 50').sort_values(by=['mean'], ascending=False)

for i in [ 1, 3 ]:
    s = best_winning_percentage.iloc[i]['setup_str']
    print('{}\n'.format(stratego.StrategoSetup(s).diagram()))
    df = pattern.equal(setups, s)
    files = df['game_id']
    print('{}\n'.format('\n'.join(files)))
    games.make_zip(files, s)

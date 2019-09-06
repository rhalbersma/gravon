#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

from gravon import archive, pattern, stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
piece_fmt = 'US'
setups = tidy.setups(games.copy(), piece_fmt)

# http://stratego-tips.blogspot.com/2019/03/python-code-to-search-gravon-archive.html
s = '86BBFB88584968BB7S993997B462934715695957'
print('{}\n'.format(stratego.SetupBoard(s, piece_fmt).diagram()))
df = pattern.equal(setups, s)
ids = df['game_id'].tolist()
print('{}\n'.format('\n'.join(ids)))
archive.make(ids, s)

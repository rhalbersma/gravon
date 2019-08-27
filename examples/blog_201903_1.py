#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

from gravon import archive, pattern, pieces, stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy(), 'US')

# http://stratego-tips.blogspot.com/2019/03/python-code-to-search-gravon-archive.html
s = '86BBFB88584968BB7S993997B462934715695957'
print('{}\n'.format(stratego.Setup(s, 'US').diagram()))
df = pattern.equal(setups, s)
print('{}\n'.format(df['game_id']))
archive.make(df, s)

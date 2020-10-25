#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://stratego-tips.blogspot.com/2017/04/top-row-open-flag-winning-game-files-at.html

import pandas as pd

from gravon import archive, pattern, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_WLD_score(setups)

center_squares = [ 'e4', 'f4' ]
outside_wings  = [ 'a4', 'j4' ]
inside_wings   = [ 'b4', 'i4' ]

for squares in [ center_squares, outside_wings, inside_wings ]:
    df = pattern.piece_on(setups.copy(), 'F', list(map(pattern.square2index, squares)))
    print('{}\n'.format(df.groupby('player').agg({
        'W': ['sum', 'count', 'mean']
    })))

    df.query('W == True', inplace=True)
    files = df['game_id'].tolist()
    print('{}\n'.format('\n'.join(files)))
    games.make_zip(files, 'W_F_' + '_'.join(squares))

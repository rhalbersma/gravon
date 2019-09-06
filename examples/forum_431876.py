#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/357378-strategy-question-findingavoiding-bombs-at-the-end-of-games/?p=431876

import pandas as pd

from gravon import archive, pattern, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_WLD_score(setups)

center_squares = [ 'e4', 'f4' ]
outside_wings  = [ 'a4', 'j4' ]
inside_wings   = [ 'b4', 'i4' ]
open_flag_front = center_squares + outside_wings + inside_wings

for squares in [ open_flag_front, center_squares ]:
    df = pattern.piece_on(setups.copy(), 'F', list(map(pattern.square2index, squares)))
    print('{}\n'.format(df.groupby('player').agg({
        'W': ['sum', 'count', 'mean']
    })))

for squares in [ center_squares ]:
    df = pattern.piece_on(setups.copy(), 'F', list(map(pattern.square2index, squares)))
    df.query('W == True', inplace=True)
    files = df['game_id'].tolist()
    print('{}\n'.format('\n'.join(files)))
    archive.make(files, 'W_F_' + '_'.join(squares))

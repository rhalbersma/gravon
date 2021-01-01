#          Copyright Rein Halbersma 2018-2021.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66390

import pandas as pd

from gravon import stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

top20 = setups['setup_str'].value_counts().to_frame(name='count').head(20)
for t in top20.itertuples():
    print('{}'.format(stratego.StrategoSetup(t.Index).diagram(sep='')))
    print(' {}\n'.format(t.count))

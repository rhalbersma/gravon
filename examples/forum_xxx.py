#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

from gravon import tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_board(setups)

# Unpublished analysis
pd.options.display.float_format = '{:7.2%}'.format
lanes = [('a4', 'b4'), ('e4', 'f4'), ('i4', 'j4')]

for lane in lanes:
    setups[lane[0]] = setups['board'].apply(lambda x: x.square(lane[0]))
    setups[lane[1]] = setups['board'].apply(lambda x: x.square(lane[1]))
    setups[lane[0] + lane[1]] = setups[lane[0]] + setups[lane[1]]

for lane in lanes:
    print('{}\n'.format(setups[lane[0]+lane[1]].value_counts(normalize=True).head(20)))
    print('{}\n'.format(pd.crosstab(setups[lane[0]], setups[lane[1]], margins=True, normalize='all')))
    print('{}\n'.format(pd.crosstab(setups[lane[0]], setups[lane[1]], margins=True, normalize='index')))
    print('{}\n'.format(pd.crosstab(setups[lane[0]], setups[lane[1]], margins=True, normalize='columns')))

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

from gravon import pattern, stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://stratego-tips.blogspot.com/2017/04/wonloss-percentage-of-every-stratego.html
setups = tidy.add_state(setups)
setups = tidy.add_WLD_score(setups)

np.set_printoptions(formatter={'float': '{:7.2%}'.format}, linewidth=100)
F = stratego.Setup.ranks['F']
count_W  = pd.Series(setups.query('W == True' )['state']).apply(lambda x: x.placement[F,:,:]).agg(['sum'])[0]
count_WL = pd.Series(setups.query('D == False')['state']).apply(lambda x: x.placement[F,:,:]).agg(['sum'])[0]
print('Won /(Won+Loss) Percentage from Every Flag Position\n')
print('{}\n'.format(np.flip(count_W / count_WL, axis=0)))
np.set_printoptions()

setups['G'] = 1
for idx in range(40):
    print('Flag Position = {}\n'.format(idx))
    df = pattern.piece_on(setups.copy(), 'F', [idx])
    print('{}\n'.format(df.groupby('player')['W', 'L', 'D', 'G'].agg(['sum'])))
    s = df.filter(['G', 'W', 'L', 'D']).agg(['sum'])
    print('{}\n'.format(s))
    WWL  = float(s['W'] / (s['W'] + s['L']))
    WWLD = float(s['W'] / (s['W'] + s['L'] + s['D']))
    print('Win/(Win+Loss) Percentage = {:5.4f} Win/(Win+Loss+Draw) Percentage = {:5.4f}\n'.format(WWL, WWLD))

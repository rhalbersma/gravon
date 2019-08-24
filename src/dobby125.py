#!/usr/bin/env python3

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

import archive
import pattern
import stratego
import tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://forum.stratego.com/topic/2429-analyzing-game-setups/?p=34049
setups = tidy.add_state(setups)
count, probs = pd.Series(setups['state']).apply(lambda x: x.placement).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:7.2%}'.format}, linewidth=100)
piece_order = [ 'F' ] + list(reversed(stratego.Setup.pieces[1:11])) + [ 'B' ]
rank_order = [ stratego.Setup.ranks[piece] for piece in piece_order ]
for row in reversed(range(4)):
    for col in range(10):
        print('{}{}:\n'.format(chr(col + ord('a')), row + 1))
        print('{}\n'.format(count[rank_order,row, col]))
        print('{}\n'.format(probs[rank_order,row, col]))
np.set_printoptions()

# http://forum.stratego.com/topic/2429-analyzing-game-setups/?p=34051
unique = setups.drop_duplicates(subset='setup')
count, probs = pd.Series(unique['state']).apply(lambda x: x.placement).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:7.2%}'.format}, linewidth=100)
piece_order = [ 'F' ] + list(reversed(stratego.Setup.pieces[1:11])) + [ 'B' ]
rank_order = [ stratego.Setup.ranks[piece] for piece in piece_order ]
for row in reversed(range(4)):
    for col in range(10):
        print('{}{}:\n'.format(chr(col + ord('a')), row + 1))
        print('{}\n'.format(count[rank_order,row, col]))
        print('{}\n'.format(probs[rank_order,row, col]))
np.set_printoptions()

# http://forum.stratego.com/topic/2429-analyzing-game-setups/?p=37268
# TODO: bombed in flag detection

# http://forum.stratego.com/topic/2429-analyzing-game-setups/?p=38121
# http://forum.stratego.com/topic/2429-analyzing-game-setups/?p=38136
setups = tidy.add_unique_piece_sides(setups)
for i, piece in enumerate(tidy.unique_pieces):
    for j, other in enumerate(tidy.unique_pieces):
        if i < j:
            print('{} and {} starting on the same side:\n'.format(piece, other))
            print('{}\n'.format(pd.value_counts(setups['side_' + piece] == setups['side_' + other], normalize=True, sort=False)))

            # More detailed analysis
            print('{}\n'.format(pd.Series(setups['side_' + piece] == 'R').corr(setups['side_' + other] == 'R')))
            print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='all')))
            print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='index')))
            print('{}\n'.format(pd.crosstab(setups['side_' + piece], setups['side_' + other], margins=True, normalize='columns')))

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66589
games['winner'].value_counts(sort=False)
games['winner'].value_counts(sort=False, normalize=True)

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66601
games['result_type'].value_counts(sort=False)

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66725
setups = tidy.add_unique_piece_distances(setups)
setups['dist_FX'].agg('mean')
setups['dist_F9'].agg('mean')
setups['dist_F1'].agg('mean')
setups['dist_19'].agg('mean')
setups['dist_1X'].agg('mean')
setups['dist_9X'].agg('mean')

# More detailed analysis
setups = tidy.add_WLD_score(setups)
setups.groupby('dist_FX').agg(['count', 'mean'])['score']
setups.groupby('dist_19').agg(['count', 'mean'])['score']

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66753
setups = tidy.add_state(setups)
count, probs = pd.Series(setups['state']).apply(lambda x: x.placement).agg(['sum', 'mean'])

unique_pieces = [ 'X', '9', '1', 'F' ]
unique_ranks = [ stratego.Setup.ranks[piece] for piece in unique_pieces ]
np.set_printoptions(formatter={'float': '{:4.3f}'.format}, linewidth=100)
print('%s\n' % np.sum(count[unique_ranks,:,:], axis=2))
print('%s\n' % np.sum(probs[unique_ranks,:,:], axis=2))
np.set_printoptions()

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=67241
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
frequent20 = atleast10.head(20)

for t in frequent20.itertuples():
    print('{}\n'.format(stratego.Setup(t.setup).diagram()))
    print('Wins = {} Losses = {} Ties = {} Games Played = {} Winning Percentage = {:5.2%}\n'.format(t.W, t.L, t.D, t.count, t.W / (t.W + t.L)))

# http://stratego-tips.blogspot.com/2017/04/common-stratego-piece-placements.html
setups = tidy.add_state(setups)
count, probs = pd.Series(setups['state']).apply(lambda x: x.placement).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:7.2%}'.format}, linewidth=100)
print('The charts below show Stratego piece placements from {:,} setups.'.format(len(setups)))
for piece in list(reversed(stratego.Setup.pieces[1:11])) + [ 'B', 'F' ]:
    r = stratego.Setup.ranks[piece]
    print('Common Stratego %s Placement\n' % stratego.Setup.names[r].capitalize())
    print('%s\n' %  np.flip(count[r,:,:], axis=1))
    print('%s\n' %  np.sum (count[r,:,:], axis=1))
    print('%s\n' %  np.flip(probs[r,:,:], axis=1))
    print('%s\n' % (np.sum (probs[r,:,:], axis=1) / stratego.Setup.counts['classic'][r]))
np.set_printoptions()

# http://stratego-tips.blogspot.com/2017/04/top-row-open-flag-winning-game-files-at.html
setups = tidy.add_WLD_score(setups)
center_squares = [ 'e4', 'f4' ]
outside_wings  = [ 'a4', 'j4' ]
inside_wings   = [ 'b4', 'i4' ]

for squares in [ center_squares, outside_wings, inside_wings ]:
    df = pattern.piece_on(setups.copy(), 'F', list(map(pattern.square2index, squares)))
    print('%s\n' % df.groupby('player').agg({
        'W': ['sum', 'count', 'mean']
    }))

    df.query('W == True', inplace=True)
    print('%s\n' % df['game_id'])
    archive.make(df, 'W_F_' + '_'.join(squares))

# http://stratego-tips.blogspot.com/2017/04/wonloss-percentage-of-every-stratego.html
setups = tidy.add_state(setups)
setups = tidy.add_WLD_score(setups)

np.set_printoptions(formatter={'float': '{:7.2%}'.format}, linewidth=100)
F = stratego.Setup.ranks['F']
count_W  = pd.Series(setups.query('W == True' )['state']).apply(lambda x: x.placement[F,:,:]).agg(['sum'])[0]
count_WL = pd.Series(setups.query('D == False')['state']).apply(lambda x: x.placement[F,:,:]).agg(['sum'])[0]
print('Won /(Won+Loss) Percentage from Every Flag Position\n')
print('%s\n' % np.flip(count_W / count_WL, axis=0))
np.set_printoptions()

setups['G'] = 1
for idx in range(40):
    print('Flag Position = {}\n'.format(idx))
    df = pattern.piece_on(setups.copy(), 'F', [idx])
    print('%s\n' % df.groupby('player')['W', 'L', 'D', 'G'].agg(['sum']))
    s = df.filter(['G', 'W', 'L', 'D']).agg(['sum'])
    print('%s\n' % s)
    WWL  = float(s['W'] / (s['W'] + s['L']))
    WWLD = float(s['W'] / (s['W'] + s['L'] + s['D']))
    print('Win/(Win+Loss) Percentage = {:5.4f} Win/(Win+Loss+Draw) Percentage = {:5.4f}\n'.format(WWL, WWLD))

# http://stratego-tips.blogspot.com/2017/05/best-winning-percentage-stratego-game.html
best_winning_percentage = atleast10.query('count >= 50').sort_values(by=['mean'], ascending=False)

for i in [ 1, 3 ]:
    s = best_winning_percentage.iloc[i]['setup']
    print('%s\n' % stratego.Setup(s).diagram())
    df = pattern.equal(setups, s)
    print('%s\n' % df['game_id'])
    archive.make(df, s)

# http://stratego-tips.blogspot.com/2017/12/marshal-blitzer-games-from-gravon.html
for i in [ 5 ]:
    s = best_winning_percentage.iloc[i]['setup']
    print('%s\n' % stratego.Setup(s).diagram())
    df = pattern.equal(setups, s)
    print('%s\n', df['game_id'])
    archive.make(df, s)

# http://stratego-tips.blogspot.com/2019/03/listing-of-most-popular-stratego-game.html
for t in atleast10.itertuples():
    print('{}\n'.format(stratego.Setup(t.setup).diagram()))
    print('Wins = {} Losses = {} Ties = {} Games Played = {} Winning Percentage = {:5.2%}\n'.format(t.W, t.L, t.D, t.count, t.W / (t.W + t.L)))

# http://stratego-tips.blogspot.com/2019/03/python-code-to-search-gravon-archive.html
board = '86BBFB88584968BB7S993997B462934715695957'
s = ''.join(stratego.US2EU(piece) for piece in board)
df = pattern.equal(setups, s)
print('%s\n', df['game_id'])
archive.make(df, s)

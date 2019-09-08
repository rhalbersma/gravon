#!/usr/bin/env python3

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import math

import numpy as np
import pandas as pd

import archive
import elo
import pattern
import strados2
import stratego
import tidy

games = pd.read_csv("../data/classic.csv")
setups = tidy.setups(games.copy())

np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
np.set_printoptions(linewidth=100)

dfR = df.query('side_X == "L" & side_9 == "L"')

matches = pattern.match(df, """
BB......BB
..........
..........
..........
""")[0]

setups = [ s.pieces for s in matches['setup_str'] ]
pieces = stratego.StrategoSetup.pieces

num_setups = len(setups)
placements = { p : sum(s == p for s in setups) for p in pieces }
 
print(num_setups)
print("Placement by piece and square")
for p, n in placements.items():
    print(p)
    print(np.round(n / num_setups, 3))
print("")

agg = matches.groupby('strados2').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']
})
agg.columns = [ col[0] for col in agg.columns.values[:-2] ] + [ agg.columns.values[-2][1], agg.columns.values[-1][0] ]

p = .5
agg['z'] = agg.apply(lambda x: (x['count'] * (x['score'] - p) / (math.sqrt(x['count'] * p * (1-p)))), axis=1)
agg['Elo'] = agg.apply(lambda x: int(round(elo.tpr(x['count'], x['score']))), axis=1)
agg.sort_values(by=['count'], ascending=False, inplace=True)
agg.sort_values(by='z', ascending=False, inplace=True)
agg.reset_index(inplace=True)

games.make_zip(*pattern.equals(matches, agg.iloc[0]['strados2']))
games.make_zip(*pattern.equals(matches, agg.iloc[1]['strados2']))

def AD_B(r: str) -> bool:
    n = [ int(c) for c in r ]
    return (3 <= (n[0] + n[1]) <= 6) and (n[0] >= 2) and (n[0] >= n[1])

setups = df
setups = setups.assign(rdistB = setups['setup_str'].apply(lambda x: stratego.StrategoSetup(x).rdist('B')))
setups = setups.assign(is_AD_B = setups['rdistB'].apply(lambda x: AD_B(x)))
setups.groupby('is_AD_B').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']    
})
rdistB = setups.groupby('rdistB').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']    
})
rdistB.columns = [ col[0] for col in rdistB.columns.values[:-2] ] + [ rdistB.columns.values[-2][1], rdistB.columns.values[-1][0] ]
rdistB.reset_index(inplace=True)
rdistB = rdistB.assign(AD = rdistB['rdistB'].apply(lambda x: AD_B(x)))

def AD_3(r: str) -> bool:
    n = [ int(c) for c in r ]
    return (2 <= n[0] <= 4) and (1 <= n[1] <= 3) and ((n[2] + n[3]) <= 2)

setups = setups.assign(rdist3 = setups['setup_str'].apply(lambda x: stratego.StrategoSetup(x).rdist('3')))
setups = setups.assign(is_AD_3 = setups['rdist3'].apply(lambda x: AD_3(x)))
setups.groupby('is_AD_3').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']    
})
rdist3 = setups.groupby('rdist3').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']    
})
rdist3.columns = [ col[0] for col in rdist3.columns.values[:-2] ] + [ rdist3.columns.values[-2][1], rdist3.columns.values[-1][0] ]
rdist3.reset_index(inplace=True)
rdist3 = rdist3.assign(AD = rdist3['rdist3'].apply(lambda x: AD_3(x)))


def AD_2r(r: str) -> bool:
    n = [ int(c) for c in r ]
    return (1 <= n[0] <= 2) and (n[3] <= 3)

setups = setups.assign(rdist2 = setups['setup_str'].apply(lambda x: stratego.StrategoSetup(x).rdist('2')))
setups = setups.assign(is_AD_2r = setups['rdist2'].apply(lambda x: AD_2r(x)))
setups.groupby('is_AD_2r').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']    
})
rdist2 = setups.groupby('rdist2').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']    
})
rdist2.columns = [ col[0] for col in rdist2.columns.values[:-2] ] + [ rdist2.columns.values[-2][1], rdist2.columns.values[-1][0] ]
rdist2.reset_index(inplace=True)
rdist2 = rdist2.assign(AD = rdist2['rdist2'].apply(lambda x: AD_2r(x)))

def AD_2c(r: str) -> bool:
    n = [ int(c) for c in r ]
    return (1 <= (n[0] + n[1] + n[4] + n[5] + n[8] + n[9]) <= 4)

setups = setups.assign(cdist2 = setups['setup_str'].apply(lambda x: stratego.StrategoSetup(x).cdist('2')))
setups = setups.assign(is_AD_2c = setups['cdist2'].apply(lambda x: AD_2c(x)))
setups.groupby('is_AD_2c').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']    
})
cdist2 = setups.groupby('cdist2').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']    
})
cdist2.columns = [ col[0] for col in cdist2.columns.values[:-2] ] + [ cdist2.columns.values[-2][1], cdist2.columns.values[-1][0] ]
cdist2.reset_index(inplace=True)
cdist2 = cdist2.assign(AD = cdist2['cdist2'].apply(lambda x: AD_2c(x)))

setups['is_AD_B32'] = setups['is_AD_B'] & setups['is_AD_3'] & setups['is_AD_2r']
setups.groupby('is_AD_B32').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']    
})

agg = setups.groupby('setup_str').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']
})
agg.columns = [ col[0] for col in agg.columns.values[:-2] ] + [ agg.columns.values[-2][1], agg.columns.values[-1][0] ]

p = .5
agg['z'] = agg.apply(lambda x: (x['count'] * (x['score'] - p) / (math.sqrt(x['count'] * p * (1-p)))), axis=1)
agg['Elo'] = agg.apply(lambda x: int(round(elo.tpr(x['count'], x['score']))), axis=1)
agg.sort_values(by=['count'], ascending=False, inplace=True)
agg.sort_values(by='z', ascending=False, inplace=True)
agg.reset_index(inplace=True)

games.make_zip(*pattern.equals(setups, agg.iloc[1]['setup_str']))
games.make_zip(*pattern.equals(setups, agg.iloc[3]['setup_str']))
games.make_zip(*pattern.equals(setups, agg.iloc[12]['setup_str']))


# Appendix D of Vincent de Boer's thesis
# http://www.kbs.twi.tudelft.nl/docs/MSc/2007/deBoer/thesis.pdf 
VdB = [ stratego.StrategoSetup(pattern.matrix2string(s)).canonical().strados2() for s in [
"""
6225263X26
54B1927782
4B4785B564
23B23BFB33
""",
"""
X653262226
4288924BB5
727165B452
73334BFBB3
""",
"""
6249622X26
5275B27783
4813B2655B
3B4B4233BF
""",
"""
2852629326
X27826B5B5
647175B4B4
32334BFB32
""",
"""
9624222362
3287B5X758
B6175265B4
423B433BFB
""",
"""
2659262X62
72B1842784
54B273565B
3B423B33BF
"""
]]

agg.query('setup in @VdB')

# df = (df
# .assign(setup_R =        StraDoS2_decode(df.field_content.str[:40]) )
# .assign(setup_B = mirror(StraDoS2_decode(df.field_content.str[60:])))
# )


def square_crosstab(df, sq1: str, sq2: str):
    df['sq1'] = df['setup_str'].apply(lambda x: x.square(sq1))
    df['sq2'] = df['setup_str'].apply(lambda x: x.square(sq2))
    return df

df1 = square_crosstab(df, 'e4', 'f4')

agg = df1.groupby(['sq1', 'sq2']).agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']
})


# print("Placement by piece and file")
# for p, n in placements.items():
#     print(p, end=": ")
#     print(np.round(np.sum(n, axis=0) / num_setups, 3))
# print("")

# print("Placement by piece and rank")
# for p, n in placements.items():
#     print(p, end=": ")
#     print(np.round(np.sum(n, axis=1) / num_setups, 3))
# print("")

# import matplotlib.pyplot as plt

# print("Placement by piece and square")
# for p, n in placements.items():
#     df = np.flip(n, axis=0) / num_setups
#     plt.figure()
#     plt.title(p)
#     plt.imshow(df, cmap='RdYlGn_r')
#     plt.show()
#     plt.close()
# print("")

# print("Placement by piece and file")
# fig, axs = plt.subplots(1, 12, sharey=True)
# for i, p in enumerate(pieces):
#     n = placements[p]
#     df = np.transpose(np.sum(n, axis=0).reshape(1, W_SETUP)) / num_setups
#     axs[i].set_title(p)
#     axs[i].get_xaxis().set_visible(False)
#     axs[i].imshow(df, cmap='RdYlGn_r')
# plt.show()
# plt.close()

# print("Placement by piece and rank")
# fig, axs = plt.subplots(1, 12, sharey=True)
# for i, p in enumerate(pieces):
#     n = placements[p]
#     df = np.flip(np.sum(n, axis=1).reshape(H_SETUP, 1), axis=0) / num_setups
#     axs[i].set_title(p)
#     axs[i].get_xaxis().set_visible(False)
#     axs[i].imshow(df, cmap='RdYlGn_r')
# plt.show()
# plt.close()

# placements = { p : np.array([ s == p for s in setups ]) for p in pieces }

# n = placements['3']
# cnts = np.sum(n, axis=1)
# for i in range(10):
#     print(np.round(np.bincount(cnts[:,i]) / num_setups, 3))

setups = setups.assign(rdist7 = setups['setup_str'].apply(lambda x: stratego.StrategoSetup(x).rdist('7')))
#setups = setups.assign(is_AD_3 = setups['rdist3'].apply(lambda x: AD_3(x)))
#setups.groupby('is_AD_3').agg({
#    'W': ['sum'],
#    'L': ['sum'],
#    'D': ['sum'],
#    'score': ['count', 'mean']    
#})
rdist7 = setups.groupby('rdist7').agg({
    'W': ['sum'],
    'L': ['sum'],
    'D': ['sum'],
    'score': ['count', 'mean']    
})
rdist7.columns = [ col[0] for col in rdist7.columns.values[:-2] ] + [ rdist7.columns.values[-2][1], rdist7.columns.values[-1][0] ]
rdist7.reset_index(inplace=True)
#rdist7 = rdist7.assign(AD = rdist7['rdist7'].apply(lambda x: AD_3(x)))

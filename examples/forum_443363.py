#          Copyright Rein Halbersma 2018-2021.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://forum.stratego.com/topic/357947-information-theory/?p=443363

import numpy as np
import pandas as pd

from gravon import archive, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())
setups = tidy.add_board(setups)

count, probs = setups['board'].apply(lambda x: x.tensor).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:6.2f}'.format}, linewidth=120)

piece_counts = np.array(pieces.counts())
random_piece_probs = piece_counts / piece_counts.sum()
random_piece_entropy = piece_counts.sum() * (-random_piece_probs * np.log2(random_piece_probs))
random_entropy = np.sum(random_piece_entropy)
gravon_square_entropy = np.sum(-probs * np.log2(probs), axis=0)
gravon_piece_entropy = np.sum(-probs * np.log2(probs), axis=(1,2))
gravon_entropy = np.sum(-probs * np.log2(probs))
delta_piece_entropy = random_piece_entropy - gravon_piece_entropy
delta_entropy = random_entropy - gravon_entropy

print('{}\n'.format(piece_counts))
print('{}\n'.format(random_piece_probs))
print('{}\n'.format(random_piece_entropy))
print('{}\n'.format(gravon_piece_entropy))
print('{}\n'.format(delta_piece_entropy))
print('{}\n'.format(delta_piece_entropy / piece_counts))
print('{}\n'.format(np.flip(gravon_square_entropy, axis=1)))

np.set_printoptions()

# Unpublished analysis
gravon_LogL = -gravon_entropy
setups['LogL'] = setups['board'].apply(lambda x: np.sum(x.tensor * np.log2(probs)))
setups['surprise'] = gravon_LogL - setups['LogL']

setups.sort_values(by=['surprise'], ascending=False, inplace=True)
setups.reset_index(drop=True, inplace=True)

games.make_zip(setups.head(10)['game_id'].tolist(), 'most_surprising')
games.make_zip(setups.tail(10)['game_id'].tolist(), 'least_surprising')

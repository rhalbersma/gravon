#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

from gravon import archive, stratego, tidy

games = pd.read_csv("../data/classic.csv").query('game_fmt == ".xml"')
setups = tidy.setups(games.copy())

# http://forum.stratego.com/topic/4470-top-20-common-game-setups-at-gravon-site/?p=66753
setups = tidy.add_board(setups)
count, probs = setups['setup_board'].apply(lambda x: x.tensor).agg(['sum', 'mean'])

np.set_printoptions(formatter={'float': '{:6.2f}'.format}, linewidth=120)

piece_counts = np.array(stratego.SetupBoard.counts['classic'])
random_piece_probs = piece_counts / 40
random_piece_entropy = 40 * (-random_piece_probs * np.log2(random_piece_probs))
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
setups['LogL'] = setups['setup_board'].apply(lambda x: np.sum(x.tensor * np.log2(probs)))
setups['surprise'] = gravon_LogL - setups['LogL']

setups.sort_values(by=['surprise'], ascending=False, inplace=True)
setups.reset_index(drop=True, inplace=True)

archive.make(setups.head(10)['game_id'].tolist(), 'most_surprising')
archive.make(setups.tail(10)['game_id'].tolist(), 'least_surprising')

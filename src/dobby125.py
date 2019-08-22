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

games = pd.read_csv("../data/classic.csv")
setups = tidy.setups(games.copy())

pieces = list(reversed(stratego.Setup.pieces[1:11])) + [ 'B', 'F' ]

# http://stratego-tips.blogspot.com/2017/04/common-stratego-piece-placements.html

placements = np.flip(sum([ setup.tensor for setup in setups['array'] ]), axis=2)
percentage = placements / len(setups)

np.set_printoptions(formatter={'float': '{:7.2%}'.format}, linewidth=150)

print(placements)
print(percentage)

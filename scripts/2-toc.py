#!/usr/bin/env python3

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import glob
import os
import sys

import pandas as pd

def main():
    data = []
    for src in glob.glob('games/*'):
        data.append(os.path.splitext(os.path.basename(src)))
    df = pd.DataFrame(data, columns=['game_id', 'game_fmt'])
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/toc.csv', index=False)

if __name__== '__main__':
    sys.exit(main())

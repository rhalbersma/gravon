#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

import gravon.package as pkg
import gravon.pattern as pattern
import gravon.archive as archive

ss2 = pkg.load_dataset('ss2')
setup = (
    """
    55X.......
    ..........
    ..........
    ..........
    """
)
games = pattern.match(ss2.query('period >= "2006-09"'), setup).sort_values(['gid', 'player'])
pd.pivot_table(games, index=['player'], columns=['match_type'], aggfunc='size', fill_value=0)
archive.make_zip(games, 'constrictor')

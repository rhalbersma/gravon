#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

import gravon.package as pkg
import gravon.pattern as pattern
import gravon.archive as archive

ss2 = pkg.load_dataset('ss2').query('type == "classic" & period >= "2006-09"')
setup = (
    """
    55X.......
    ..........
    ..........
    ..........
    """
)
games = pattern.match(ss2, setup)
pd.crosstab(games.player, games.match_type, margins=True)
archive.make_zip(games.filename.tolist(), 'constrictor')

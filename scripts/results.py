#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

import gravon.results
import gravon.strados2
import gravon.utils
import gravon.wget

def init_results() -> pd.DataFrame:
    games = gravon.load_dataset('games')
    months = list(games.query('filename.str.endswith(".xml")').drop_duplicates(subset=['date'])['date'])
    results = pd.concat([
        gravon.results.monthly(*month.split('-'))
        for month in months
    ])
    gravon.utils.save_dataset(results, 'results')
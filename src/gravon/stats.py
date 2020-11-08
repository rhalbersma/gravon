#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd

def setup_placement(df: pd.DataFrame, func=None, column='setup') -> np.array:
    # Tensors are stored as type np.int8 to save storage.
    # To avoid integer overflow, expand them to type int.
    return df[f'{column}_obj'].apply(lambda x: x.tensor.astype(int)).agg(func)

league_table = {
    'Games' : ('result', 'count'),
    'Wins'  : ('win',    'sum'  ),
    'Draws' : ('draw',   'sum'  ),
    'Losses': ('loss',   'sum'  ),
    'Score' : ('score',  'mean' )
}

score_pct = {
    'Score': '{:.2%}'
}

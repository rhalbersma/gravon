#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from typing import List

import numpy as np
import pandas as pd

def setup_ranks(df: pd.DataFrame, func=None, column='setup_obj') -> np.array:
    return df[column].apply(lambda x: x.tensor.astype(int)).agg(func)

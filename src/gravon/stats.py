#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from typing import Tuple

import numpy as np
import pandas as pd

def setup_placement(df: pd.DataFrame, func=None, column='setup_obj') -> np.array:
    # Tensors are stored as type np.int8 to save storage.
    # To avoid integer overflow, expand them to type int.
    return df[column].apply(lambda x: x.tensor.astype(int)).agg(func)

Square = Tuple[int, int]

def unique_square_where(condition: np.array) -> Square:
    return tuple(np.transpose(np.where(condition))[0])

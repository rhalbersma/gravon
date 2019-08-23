#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

def board2string(pat2d: str) -> str:
    return ''.join(reversed(pat2d.splitlines()))

def square2index(sq: str) -> int:
    row = ord(sq[1]) - ord('1')
    col = ord(sq[0]) - ord('a')
    return 10 * row + col

def equal(df: pd.DataFrame, pat2d: str, var: str='setup') -> pd.DataFrame:
    pat = board2string(pat2d)
    return df.query(var + ' == @pat')

def match(df: pd.DataFrame, pat2d: str, var: str='setup') -> pd.DataFrame:
    pat = board2string(pat2d)
    return df.query(var + '.str.match(@pat)')

def piece_on(df: pd.DataFrame, piece: str, indices: list, var: str='setup') -> pd.DataFrame:
    pred = lambda x: any(x[idx] == piece for idx in indices)
    return df.loc[lambda x: x[var].apply(pred)]

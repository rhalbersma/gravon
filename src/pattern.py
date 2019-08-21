#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

def board2string(pat2d: str) -> str:
    return ''.join(reversed(pat.splitlines()))

def equal(df: pd.DataFrame, pat2d: str, var: str='string') -> pd.DataFrame:
    pat = board2string(pat2d)
    return df.query(var + ' == @pat')

def match(df: pd.DataFrame, pat2d: str, var: str='string') -> pd.DataFrame:
    pat = board2string(pat2d)
    return df.query(var + '.str.match(@pat)')

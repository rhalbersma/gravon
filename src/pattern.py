#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd
import stratego

def equals(df: pd.DataFrame, s: str):
    return df.query('strados2 == @s'), s

def match(df: pd.DataFrame, pat: str):
    return df.query('strados2.str.match(@pat)'), pat

def board2string(p: str) -> str:
    return ''.join(reversed(p.splitlines()[1:]))

def position(df: pd.DataFrame, p: str):
    s = board2string(p)
    s = stratego.Setup(s).canonical().strados2()
    return equals(df, s)

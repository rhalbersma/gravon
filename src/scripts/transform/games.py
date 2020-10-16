#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import re
from typing import Tuple

import pandas as pd

import gravon.package as pkg

import scripts.extract.games as games
import scripts.transform.parse as parse
import scripts.transform.label as label

def get_st2() -> pd.DataFrame:
    try:
        st2 = pkg.load_dataset('st2')
    except:
        st2 = (games
            .get_txt_files()[0]
            .pipe(parse.txt_files)
            .pipe(label.txt_files)
        )
        pkg.save_dataset(st2, 'st2')
    return st2

def get_si2_sg2() -> Tuple[pd.DataFrame, pd.DataFrame]:
    try:
        si2 = pkg.load_dataset('si2')
        sg2 = pkg.load_dataset('sg2')
    except:
        st2 = get_st2()
        si2, sg2 = label.index_games(parse.index_games(st2))
        pkg.save_dataset(si2, 'si2')
        pkg.save_dataset(sg2, 'sg2')
    return si2, sg2

def get_all() -> None:
    get_st2()
    get_si2_sg2()

def remove_st2() -> bool:
    try:
        pkg.remove_dataset('st2')
        return True
    except:
        return False

def remove_si2_sg2() -> bool:
    try:
        pkg.remove_dataset('si2')
        pkg.remove_dataset('sg2')
        return True
    except:
        return False

def remove_all() -> None:
    remove_st2()
    remove_si2_sg2()


#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd


def pat1d_identity(pat2d: str) -> str:
    return ''.join([ 
        line.strip() 
        for line in pat2d.splitlines()[::-1] 
    ])


def pat1d_mirrored(pat2d: str) -> str:
    return ''.join([ 
        line.strip()[::-1] 
        for line in pat2d.splitlines()[::-1] 
    ])


def equal(df: pd.DataFrame, pat2d: str, column='setup_str', mirrored=True, by=['gid', 'player']) -> pd.DataFrame:
    return (pd
        .concat([
            df.query(f'{column} == @pat1d_identity(@pat2d)').assign(match_type = 'identity'),
            df.query(f'{column} == @pat1d_mirrored(@pat2d)').assign(match_type = 'mirrored') if mirrored else pd.DataFrame()
        ])
        .sort_values(by)
    )


def match(df: pd.DataFrame, pat2d: str, column='setup_str', mirrored=True, by=['gid', 'player']) -> pd.DataFrame:
    return (pd
        .concat([
            df.query(f'{column}.str.match(@pat1d_identity(@pat2d))').assign(match_type = 'identity'),
            df.query(f'{column}.str.match(@pat1d_mirrored(@pat2d))').assign(match_type = 'mirrored') if mirrored else pd.DataFrame()
        ])
        .sort_values(by)
    )


any_setup = (
    """
    ..........
    ..........
    ..........
    ..........
    """
)

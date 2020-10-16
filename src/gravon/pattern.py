#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

import scripts.transform.setups as setups

def serial(pat2d: str) -> str:
    return ''.join([ 
        line.strip() 
        for line in pat2d.splitlines()[::-1] 
    ])

def mirror(pat2d: str) -> str:
    return ''.join([ 
        line.strip()[::-1] 
        for line in pat2d.splitlines()[::-1] 
    ])

def equal(df: pd.DataFrame, pat2d: str, column='setup', mirrored=True) -> pd.DataFrame:
    pattern_serial = serial(pat2d)
    equaled_serial = df.query(column + '== @pattern_serial')    
    if mirrored:
        pattern_mirror = mirror(pat2d)
        equaled_mirror = df.query(column + '== @pattern_mirror)')
    else:
        equaled_mirror = pd.DataFrame()
    return (pd
        .concat([
            equaled_serial,
            equaled_mirror
        ])
        .sort_values(['gid', 'player'])
    )

def match(df: pd.DataFrame, pat2d: str, column='setup', mirrored=True) -> pd.DataFrame:
    pattern_serial = serial(pat2d)
    matched_serial = df.query(column + '.str.match(@pattern_serial)')    
    if mirrored:
        pattern_mirror = mirror(pat2d)
        matched_mirror = df.query(column + '.str.match(@pattern_mirror)')
    else:
        matched_mirror = pd.DataFrame()
    return (pd
        .concat([
            matched_serial,
            matched_mirror
        ])
        .sort_values(['gid', 'player'])
    )

#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

def pvsp(df: pd.DataFrame) -> pd.DataFrame:
    return (df
        .pipe(lambda x: x.set_axis(x
            .columns
            .str.lower()
            .str.replace(' ', '_')
            , axis='columns'
        ))    
        .rename(columns = {
            'date.1'    : 'time',
            'player_1'  : 'player_red',
            'player_2'  : 'player_blue',
            'result.1'  : 'ending',
            '#_of_turns': 'turns'
        })
        .loc[:, [
            'date', 'time', 'type', 'player_red', 'player_blue', 'result', 'ending', 'turns', 'duration', 'ranked'
        ]]
    )

def results(df: pd.DataFrame) -> pd.DataFrame:
    return (df
        .pipe(lambda x: x.set_axis(x
            .columns
            .str.lower()
            .str.replace(' ', '_')
            , axis='columns'
        ))    
        .reset_index()
        .rename(columns = {
            'index'     : 'gid',
            '#_of_turns': 'num_turns'
        })
        .loc[:, [
            'gid', 'date', 'time', 'type', 'player_red', 'player_blue', 'result', 'ending', 'turns', 'duration'
        ]]
    )

def players(df: pd.DataFrame) -> pd.DataFrame:
    return (pd.wide_to_long(df
            .loc[:, [
                'gid', 'player_red', 'player_blue', 'result'
            ]]
            .replace({'result': {r'1': '2'}}, regex=True)
            .replace({'result': {'draw': '1 : 1'}})
            .assign(result_red = lambda x: x.result.str.split(' : ').str[0])
            .assign(result_blue = lambda x: x.result.str.split(' : ').str[1])
            .drop(columns='result')
            , ['player_', 'result_']
            , i='gid'
            , j='color'
            , suffix='(red|blue)'
        )
        .reset_index()
        .sort_values(['gid', 'color'], ascending=[True, False])
        .reset_index(drop=True)
        .pipe(lambda x: x.set_axis(x.columns.str.replace('_', ''), axis='columns'))
        .astype(dtype={'result': float})
        .pipe(lambda x: x.assign(result = x.result / 2))
    )

def unique_pvsp(df: pd.DataFrame) -> pd.DataFrame:
    return (df
        .loc[:, ['gid', 'player']]
        .sort_values(['gid', 'player'])
        .reset_index(drop=True)
        .assign(pid = lambda p: p.index % 2 + 1)
        .replace({'pid': {1: 'nick1', 2: 'nick2'}})
        .pivot(index='gid', columns='pid', values='player')
        .sort_values(['nick1', 'nick2'])
        .drop_duplicates()
        .reset_index(drop=True)
    )

def missing_ending_turns(df: pd.DataFrame) -> pd.DataFrame:
    return (df
        .query('ending.isnull() | turns.isnull()')
        .loc[:, ['gid']]
    )

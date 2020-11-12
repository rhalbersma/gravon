#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import pkg_resources
from typing import List

import pandas as pd


def _get_data_home() -> str:
    return pkg_resources.resource_filename(__name__, 'data')


def _get_resource(path: str) -> str:
    return os.path.join(_get_data_home(), path)


def _get_dataset(path: str) -> str:
    return _get_resource(''.join((path, '.pkl')))


def get_dataset_names() -> List[str]:
    return [
        os.path.splitext(filename)[0]
        for filename in os.listdir(_get_data_home())
        if filename.endswith('.pkl')
    ]


def load_dataset(name: str, **kws) -> pd.DataFrame:
    return pd.read_pickle(_get_dataset(name), **kws)


def save_dataset(df: pd.DataFrame, name: str, **kws) -> None:
    pd.to_pickle(df, _get_dataset(name), **kws)


def remove_dataset(name: str) -> None:
    os.remove(_get_dataset(name))


gravon_url = 'http://www.gravon.de'
player_url = f'{gravon_url}/webstart/strados2/strados2.jnlp'
strados2_url = f'{gravon_url}/strados2/files/'
stratego_url = f'{gravon_url}/gravon/stratego'

games_dir = _get_resource('games')
txt_dir = os.path.join(games_dir, 'txt')
zip_dir = os.path.join(games_dir, 'zip')
archive_dir = os.path.join(games_dir, 'archive')

results_dir = _get_resource('results')
daily_dir = os.path.join(results_dir, 'daily')

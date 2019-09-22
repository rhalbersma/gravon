#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import glob
import itertools
import os
import pkg_resources
import shutil
import zipfile

import pandas as pd

def extract(name: str, pattern: str, path: str) -> None:
    """
    Examples:
        >>> extract('downloads', '*.zip', 'games')
    """
    assert os.path.isdir(name)
    os.makedirs(path, exist_ok=True)
    for file in glob.glob(os.path.join(name, pattern)):
        with zipfile.ZipFile(file) as src:
            src.extractall(path)

def flatten(path: str) -> None:
    """
    Examples:
        >>> flatten('games')
    """
    assert os.path.isdir(path)
    for dirpath, dirnames, filenames in itertools.islice(os.walk(path), 1, None):
        for filename in filenames:
            shutil.move(os.path.join(dirpath, filename), os.path.join(path, filename))
    for dirpath, dirnames, filenames in os.walk(path):
        for d in dirnames:
            nested = os.path.join(dirpath, d)
            assert not os.listdir(nested)
            shutil.rmtree(nested)
    assert all([
        os.path.isfile(os.path.join(path, basename))
        for basename in os.listdir(path)
    ])


def to_frame(path: str, pattern: str, parser) -> pd.DataFrame:
    assert os.path.isdir(path)
    return pd.DataFrame(
        data=[parser(file) for file in glob.glob(os.path.join(path, pattern))],
        columns=['filename', 'game_type', 'date', 'id', 'field_content', 'moves', 'player_id1', 'player_id2', 'result_type', 'result_winner']
    )

def get_resource(basename: str) -> str:
    return pkg_resources.resource_filename(__name__, os.path.join('data', basename))

def save_dataset(df: pd.DataFrame, name: str) -> None:
    df.to_pickle(get_resource(name + '.pkl'))

def load_dataset(name: str) -> pd.DataFrame:
    return pd.read_pickle(get_resource(name + '.pkl'))

#          Copyright Rein Halbersma 2018-2021.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import datetime as dt
import os.path  as osp
import zipfile  as zf

import pandas as pd
from tqdm import tqdm


def _infolist(dirname: str, basename: str) -> pd.DataFrame:
    return pd.DataFrame(
        data=[
            (basename, osp.basename(mem.filename), dt.datetime(*mem.date_time).date())
            for mem in zf.ZipFile(osp.join(dirname, basename)).infolist()
            if not mem.is_dir()
        ],
        columns=[
            'name', 'filename', 'modified'
        ]
    )


def infolist(dirname: str, zip_files: pd.DataFrame) -> pd.DataFrame:
    return (zip_files
        .merge(pd
            .concat([
                    _infolist(dirname, row.name)
                    for row in zip_files.itertuples()
                ],
                ignore_index=True
            ),
            how='left', on='name', validate='one_to_many'
        )
    )


def _extract(dirname: str, basename: str, path: str) -> None:
    with zf.ZipFile(osp.join(dirname, basename)) as src:
        for mem in src.infolist():
            if not mem.is_dir():
                mem.filename = osp.basename(mem.filename)
                src.extract(mem, path)


def extract(dirname: str, zip_files: pd.DataFrame, path: str) -> None:
    for row in tqdm(zip_files.itertuples(), total=zip_files.shape[0]):
        _extract(dirname, row.name, path)


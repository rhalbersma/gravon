#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import datetime as dt
import os.path as osp
import zipfile as zf

import pandas as pd
from tqdm import tqdm

import gravon.package as pkg

def infolist(name: str) -> pd.DataFrame:
    return (pd
        .DataFrame(
            data=[
                (name, osp.basename(mem.filename), dt.datetime(*mem.date_time).date())
                for mem in zf.ZipFile(osp.join(pkg.zip_dir, name)).infolist()
                if not mem.is_dir()
            ],
            columns=[
                'name', 'filename', 'modified'
            ]
        )
    )

def extractall(files: pd.DataFrame, path: str) -> None:
    for row in tqdm(files.itertuples(), total=files.shape[0]):
        with zf.ZipFile(osp.join(pkg.zip_dir, row.name)) as src:
            for mem in src.infolist():
                if not mem.is_dir():
                    mem.filename = osp.basename(mem.filename)
                    src.extract(mem, path)

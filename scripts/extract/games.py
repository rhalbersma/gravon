#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import re

import numpy as np
import pandas as pd
from tqdm import tqdm

import gravon.package as pkg
import gravon.extract.scrape as scrape
import gravon.extract.unpack as unpack

if 'strados2.jnlp' not in os.listdir(pkg.games_dir):
    scrape.download(pkg.games_dir, 'https://www.gravon.de/webstart/strados2/strados2.jnlp')

if 'zip_files' in pkg.get_dataset_names():
    zip_files = pkg.load_dataset('zip_files')
else:
    zip_files = (scrape
        .mirror_no_directories(pkg.zip_dir, '*.zip', 'http://www.gravon.de/strados2/files/')
        .rename(columns={
            'name'         : 'zip_name',
            'last_modified': 'zip_date'
        })
    )
    pkg.save_dataset(zip_files, 'zip_files')

if 'txt_files' in pkg.get_dataset_names():
    txt_files = pkg.load_dataset('txt_files')
else:
    txt_files = (zip_files
        .merge(pd
            .concat([
                unpack.infolist(row.zip_name)
                for row in zip_files.itertuples()
            ]),
            how='left', on='zip_name', validate='one_to_many'
        )
        .reset_index(drop=True)
        .assign(
            splitext  = lambda r: r.filename.apply(lambda x: os.path.splitext(x)),
            root      = lambda r: r.splitext.apply(lambda x: x[0]),
            splitroot = lambda r: r.apply(lambda x: re.split(r'[-.]', x.root), axis=1),
            prefix    = lambda r: r.splitroot.apply(lambda x: x[0]),
            type      = lambda r: r.prefix,
            period    = lambda r: r.splitroot.apply(lambda x: '-'.join(
                np.where(
                    x[2] == '0', 
                    [ str(int(x[1]) - 1), '12' ] + x[3:-1], # transform 20xy-0 to 20xz-12 with z = y - 1
                    [ x[1], str(x[2]).zfill(2) ] + x[3:-1]  # transform 20xy-z to 20xy-0z if z < 10
                )
            )),
            freq = lambda r: r.period.apply(lambda x: np.where(len(x) == 10, 'D', 'M')),
            no   = lambda r: r.splitroot.apply(lambda x: int(x[-1])),
            ext  = lambda r: r.splitext.apply(lambda x: x[1])
        )
        .replace({'type': {                
            'classic'           : 0,
            'barrage'           : 1,
            'freesetup'         : 2,
            'classicfree'       : 2,
            'ultimate'          : 3,
            'ultimate lightning': 3,
            'duell'             : 4
        }})
        .drop(columns=['splitext', 'root', 'splitroot'])
        .sort_values(['type', 'period', 'no'])
        .reset_index(drop=True)
        .reset_index()
        .rename(columns={'index': 'gid'})
        .loc[:, [
            'gid', 'url', 'zip_name', 'zip_date', 'txt_date', 'filename', 'prefix', 'type', 'period', 'freq', 'no', 'ext'
        ]]        
    )
    pkg.save_dataset(txt_files, 'txt_files')

for row in tqdm(zip_files.itertuples(), total=zip_files.shape[0]):
    unpack.extractall(row.zip_name, pkg.txt_dir)

if 'repaired' in pkg.get_dataset_names():
    pkg.remove_dataset('repaired')


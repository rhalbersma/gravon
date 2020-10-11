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
    scrape.download(pkg.games_dir, pkg.player_url)

zip_files_remote = scrape.list_directory_contents_recursive(pkg.strados2_url)
try:
    zip_files_local = pkg.load_dataset('zip_files')
except:
    os.makedirs(pkg.zip_dir)
    zip_files_local = pd.DataFrame(columns=zip_files_remote.columns.values)
assert sorted(zip_files_local.name) == sorted(os.listdir(pkg.zip_dir))
download_queue = (pd
    .merge(
        zip_files_remote, zip_files_local, 
        how='outer', indicator=True, validate='one_to_one'
    )
    .query('_merge == "left_only"')
    .drop(columns='_merge')
)
downloaded = scrape.mirror_no_directories(pkg.zip_dir, '*.zip', download_queue)
zip_files = zip_files_remote
if not downloaded.empty:
    pkg.save_dataset(zip_files, 'zip_files')
assert sorted(zip_files.name) == sorted(os.listdir(pkg.zip_dir))

txt_files = (zip_files
    .merge(pd
        .concat([
                unpack.infolist(row.name)
                for row in zip_files.itertuples()
            ],
            ignore_index=True
        ),
        how='left', on='name', validate='one_to_many'
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
        'gid', 'url', 'name', 'last_modified', 'date', 'filename', 'prefix', 'type', 'period', 'freq', 'no', 'ext'
    ]]        
)
pkg.save_dataset(txt_files, 'txt_files')

if sorted(txt_files.filename) != sorted(os.listdir(pkg.txt_dir)):
    for row in tqdm(zip_files.itertuples(), total=zip_files.shape[0]):
        unpack.extractall(row.name, pkg.txt_dir)

try:
    pkg.remove_dataset('repaired')
except:
    pass


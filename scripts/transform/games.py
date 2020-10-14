#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import re

import numpy as np

import gravon.package          as pkg
import gravon.transform.repair as repair
import gravon.transform.parse  as parse
import gravon.transform.label  as label

txt_files = (pkg
    .load_dataset('txt_files')
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
        freq      = lambda r: r.period.apply(lambda x: np.where(len(x) == 10, 'D', 'M')),
        no        = lambda r: r.splitroot.apply(lambda x: int(x[-1])),
        ext       = lambda r: r.splitext.apply(lambda x: x[1])
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
        'gid', 'url', 'name', 'last_modified', 'modified', 'filename', 'prefix', 'type', 'period', 'freq', 'no', 'ext'
    ]]        
)

try:
    repaired = pkg.load_dataset('repaired')
except:
    repaired = repair.directory(txt_files)
    pkg.save_dataset(repaired, 'repaired')

try:
    parsed_index = pkg.load_dataset('parsed_index')
    parsed_games = pkg.load_dataset('parsed_games')
except:
    parsed_index, parsed_games = parse.index_games(txt_files)
    pkg.save_dataset(parsed_index, 'parsed_index')
    pkg.save_dataset(parsed_games, 'parsed_games')

si2 = label.index(txt_files.merge(parsed_index, on=['gid', 'type'], validate='one_to_one'))
sg2 = label.games(parsed_games)
pkg.save_dataset(si2, 'si2')
pkg.save_dataset(sg2, 'sg2')

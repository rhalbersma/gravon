#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
from typing import Tuple

import pandas as pd

import gravon.package as pkg

import scripts.extract.scrape as scrape
import scripts.extract.unpack as unpack
import scripts.extract.repair as repair

def get_zip_files() -> Tuple[pd.DataFrame, pd.DataFrame]:
    zip_files_remote = scrape.list_directory_contents_recursive(pkg.strados2_url)
    try:
        zip_files_cached = pkg.load_dataset('zip_files')
    except:
        os.makedirs(pkg.zip_dir)
        zip_files_cached = pd.DataFrame(columns=zip_files_remote.columns.values)
    assert sorted(os.listdir(pkg.zip_dir)) == sorted(zip_files_cached.name)
    zip_queue = (pd
        .merge(
            zip_files_remote, zip_files_cached, 
            how='outer', indicator=True, validate='one_to_one'
        )
       .query('_merge == "left_only"')
        .drop(columns='_merge')
    )
    scraped, zip_files = scrape.mirror_no_directories(pkg.zip_dir, '*.zip', zip_queue), zip_files_remote
    if not scraped.empty:
        pkg.save_dataset(zip_files, 'zip_files')
    assert sorted(os.listdir(pkg.zip_dir)) == sorted(zip_files.name)
    return zip_files, scraped

def get_txt_files() -> Tuple[pd.DataFrame, pd.DataFrame]:
    zip_files, _ = get_zip_files()
    txt_files_packed = unpack.infolist(pkg.zip_dir, zip_files)
    try:
        txt_files_cached = pkg.load_dataset('txt_files')
    except:
        os.makedirs(pkg.txt_dir)
        txt_files_cached = pd.DataFrame(columns=txt_files_packed.columns.values)
    assert sorted(os.listdir(pkg.txt_dir)) == sorted(txt_files_cached.filename)
    txt_queue = (pd
        .merge(
            txt_files_packed, txt_files_cached, 
            how='outer', indicator=True, validate='one_to_one'
        )
        .query('_merge == "left_only"')
        .drop(columns='_merge')
    )
    zip_queue = txt_queue.drop_duplicates('name')
    unpack.extract(pkg.zip_dir, zip_queue, pkg.txt_dir)
    unpacked, txt_files = txt_queue.loc[:, ['filename']], txt_files_packed
    if not unpacked.empty:
        pkg.save_dataset(txt_files, 'txt_files')
    assert sorted(os.listdir(pkg.txt_dir)) == sorted(txt_files.filename)
    return txt_files, unpacked

def fix_txt_files() -> pd.DataFrame:
    txt_files, _ = get_txt_files()
    repaired = repair.directory(pkg.txt_dir, txt_files)
    if not repaired.empty:
        pkg.save_dataset(repaired, 'repaired')
    return repaired

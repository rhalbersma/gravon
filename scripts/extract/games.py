#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os

import pandas as pd

import gravon.package        as pkg
import gravon.extract.scrape as scrape
import gravon.extract.unpack as unpack

def get_zip_files() -> pd.DataFrame:
    zip_files_remote = scrape.list_directory_contents_recursive(pkg.strados2_url)
    try:
        zip_files_cached = pkg.load_dataset('zip_files')
    except:
        os.makedirs(pkg.zip_dir)
        zip_files_cached = pd.DataFrame(columns=zip_files_remote.columns.values)
    assert sorted(os.listdir(pkg.zip_dir)) == sorted(zip_files_cached.name)
    scrape_queue = (pd
        .merge(
            zip_files_remote, zip_files_cached, 
            how='outer', indicator=True, validate='one_to_one'
        )
       .query('_merge == "left_only"')
        .drop(columns='_merge')
    )
    scraped = scrape.mirror_no_directories(scrape_queue, '*.zip', pkg.zip_dir)
    zip_files = zip_files_remote
    if not scraped.empty:
        pkg.save_dataset(zip_files, 'zip_files')
    assert sorted(os.listdir(pkg.zip_dir)) == sorted(zip_files.name)
    return zip_files

def get_txt_files(zip_files=None) -> pd.DataFrame:
    if zip_files is None:
        zip_files = get_zip_files()
    txt_files_packed = (zip_files
        .merge(pd
            .concat([
                    unpack.infolist(row.name)
                    for row in zip_files.itertuples()
                ],
                ignore_index=True
            ),
            how='left', on='name', validate='one_to_many'
        )
    )
    try:
        txt_files_cached = pkg.load_dataset('txt_files')
    except:
        os.makedirs(pkg.txt_dir)
        txt_files_cached = pd.DataFrame(columns=txt_files_packed.columns.values)
    assert sorted(os.listdir(pkg.txt_dir)) == sorted(txt_files_cached.filename)
    unpack_queue = (pd
        .merge(
            txt_files_packed, txt_files_cached, 
            how='outer', indicator=True, validate='one_to_one'
        )
        .query('_merge == "left_only"')
        .drop(columns='_merge')
        .drop_duplicates('name')
    )
    unpack.extractall(unpack_queue, pkg.txt_dir)
    txt_files = txt_files_packed
    if not unpack_queue.empty:
        pkg.save_dataset(txt_files, 'txt_files')
        try:
            pkg.remove_dataset('repaired')
        except:
            pass
    assert sorted(os.listdir(pkg.txt_dir)) == sorted(txt_files.filename)
    return txt_files

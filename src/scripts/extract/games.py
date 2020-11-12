#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import shutil
from typing import Tuple

import pandas as pd

import gravon.package as pkg

import scripts.extract.scrape as scrape
import scripts.extract.unpack as unpack
import scripts.extract.repair as repair


def get_player() -> bool:
    if not os.path.exists(pkg.games_dir) or 'strados2.jnlp' not in os.listdir(pkg.games_dir):
        scrape.download(pkg.games_dir, pkg.player_url)
        return True
    return False


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


def get_txt_files() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
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
    repaired = repair.directory(pkg.txt_dir, unpacked)
    return txt_files, unpacked, repaired


def get_all() -> pd.DataFrame:
    get_player()
    get_zip_files()
    *_, repaired = get_txt_files()
    return repaired


def remove_player() -> bool:
    try:
        os.remove(os.path.join(pkg.games_dir, 'strados2.jnlp'))
        return True
    except:
        return False


def remove_zip_files() -> bool:
    try:
        shutil.rmtree(pkg.zip_dir, ignore_errors=True)
        pkg.remove_dataset('zip_files')
        return True
    except:
        return False


def remove_txt_files() -> bool:
    try:
        shutil.rmtree(pkg.txt_dir, ignore_errors=True)
        pkg.remove_dataset('txt_files')
        return True
    except:
        return False


def remove_all() -> None:
    remove_player()
    remove_zip_files()
    remove_txt_files()
    shutil.rmtree(pkg.games_dir, ignore_errors=True)


#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import shutil

def make(files: list, id: str, games_dir: str='../games/', archive_root: str='../archives/') -> None:
    os.makedirs(archive_root, exist_ok=True)
    archive_dir = archive_root + id
    os.makedirs(archive_dir, exist_ok=True)
    for f in files:
        shutil.copy(games_dir + f + '.xml', archive_dir)
    shutil.make_archive(archive_dir, 'zip', root_dir=archive_dir)
    shutil.rmtree(archive_dir)

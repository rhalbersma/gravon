#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import shutil

def make(files, id: str, games_dir: str='../games/', archive_root: str='../archives/'):
    archive_dir = archive_root + id
    if not os.path.exists(archive_dir):
        os.mkdir(archive_dir)
    for f in files['game_id']:
        shutil.copy(games_dir + f, archive_dir)
    shutil.make_archive(archive_dir, 'zip', root_dir=archive_dir)
    shutil.rmtree(archive_dir)

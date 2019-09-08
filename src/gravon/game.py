#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import shutil

class Archive:
    def make_zip(files: list, base_name: str, games_dir: str, archives_dir: str) -> str:
        """Create a zip file and return its name."""
        assert os.path.exists(games_dir)
        os.makedirs(archives_dir, exist_ok=True)
        base_dir = os.path.join(archives_dir, base_name)
        os.makedirs(base_dir, exist_ok=True)
        for file in files:
            src = os.path.join(games_dir, file)
            if os.path.exists(src):
                shutil.copy(src, base_dir)
        result = shutil.make_archive(base_name, 'zip', archive_dir, base_dir)
        shutil.rmtree(base_dir)
        return result

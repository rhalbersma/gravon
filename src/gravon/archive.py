#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import shutil
from typing import List

import gravon.package as pkg

def make_zip(filenames: List[str], base_dir: str) -> None:
    os.makedirs(pkg.archive_dir, exist_ok=True)
    base_name = os.path.join(pkg.archive_dir, base_dir)
    os.makedirs(base_name, exist_ok=True)
    for filename in filenames:
        src = os.path.join(pkg.txt_dir, filename)
        if os.path.exists(src):
            shutil.copy(src, base_name)
    shutil.make_archive(base_name, 'zip', base_name)
    shutil.rmtree(base_name)

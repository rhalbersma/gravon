#!/usr/bin/env python

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import glob
import itertools
import os
import shutil
import sys
import zipfile

def main():
    downloads = 'downloads'
    format = 'zip'
    games = 'games'

    # unpack all '.zip' files from the 'downloads' directory into the 'games' directory
    os.makedirs(games, exist_ok=True)
    for f in glob.glob(os.path.join(downloads, '*.' + format)):
        with zipfile.ZipFile(f) as r:
            r.extractall(games)

    # flatten 'games' directory
    for dirpath, dirnames, filenames in itertools.islice(os.walk(games), 1, None):
        for f in filenames:
            shutil.move(os.path.join(dirpath, f), games)

    # remove nested 'games' directories
    for dirpath, dirnames, filenames in os.walk(games):
        for d in dirnames:
            nested = os.path.join(dirpath, d)
            assert not os.listdir(nested)
            shutil.rmtree(nested)

    # replace spaces with underscores in filenames
    for f in os.listdir(games):
        src = os.path.join(games, f)
        dst = os.path.join(games, f).replace(' ', '_')
        os.rename(src, dst)

if __name__== '__main__':
    sys.exit(main())

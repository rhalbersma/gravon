#!/usr/bin/env python3

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import glob
import os
import shutil
import sys
import zipfile

import pandas as pd

def flatten(target_dir, sub_dirs):
    for sub_dir in sub_dirs:
        target_sub_dir = target_dir + sub_dir
        for src in os.listdir(target_sub_dir):
            shutil.move(target_sub_dir + src, target_dir + src)
        os.rmdir(target_sub_dir)

def main():
    # unpack all .zip files into a "games" directory
    os.makedirs('games', exist_ok=True)
    for f in glob.glob('downloads/*.zip'):
        with zipfile.ZipFile(f) as r:
            r.extractall('games')

    # flatten games directory and remove nested directories
    flatten('games/', ['barrage/', 'classic/', 'ultimate/'])
    
    # remove spaces from ultimate lightning file names
    for f in os.listdir('games'):
        os.rename(os.path.join('games', f), os.path.join('games', f).replace(' ', '_').lower())

    # rename game type "duell" to "barrage" since the former cannot be read by the StraDoS2 viewer
    # sed -i 's/duell/barrage/g' duell-*

if __name__== '__main__':
    sys.exit(main())

#!/bin/bash

# unpack all .zip files into a "games" directory
unzip -qq "downloads/*.zip" -d games

# flatten games directory and remove nested directories
cd games
find . -mindepth 2 -type f -print0 | xargs -0 mv -t .
find . -mindepth 1 -type d -print0 | xargs -0 rmdir

# remove spaces from ultimate lightning file names
find . -print0 | xargs -0 rename 's/ /_/g'

# rename game type "duell" to "barrage" since the former cannot be read by the StraDoS2 viewer
sed -i 's/duell/barrage/g' duell-*

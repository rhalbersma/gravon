#!/bin/bash

mkdir -p data
scripts/xml2csv.py data/barrage.csv  games/barrage*
scripts/xml2csv.py data/classic.csv  games/classic[.-]*
scripts/xml2csv.py data/duell.csv    games/duell*
scripts/xml2csv.py data/free.csv     games/*free*
scripts/xml2csv.py data/ultimate.csv games/ultimate*

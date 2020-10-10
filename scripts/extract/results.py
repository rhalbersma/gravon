#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import datetime as dt
import os

import pandas as pd
from tqdm import tqdm

import gravon.package as pkg
import gravon.extract.scrape as scrape

if os.path.exists(pkg.daily_dir) and 'results' in pkg.get_dataset_names():
    last = dt.date(*map(int, sorted(os.listdir(pkg.daily_dir))[-1].split('.')[0].split('-')[1:]))
    results = pkg.load_dataset('results')
    assert last == dt.date(*map(int, results.date.max().split('-')))
    start = last + dt.timedelta(days=1)
else:
    assert not os.path.exists(pkg.daily_dir) and 'results' not in pkg.get_dataset_names()
    results = pd.DataFrame()
    start = dt.date(2003, 6, 1)

files = scrape.results(pkg.daily_dir, start, pd.to_datetime('today').date())   
if files:
    update = (pd
        .concat([
            pd.read_csv(os.path.join(pkg.daily_dir, file))
            for file in tqdm(files)
        ], ignore_index=True)
        .pipe(lambda x: x.set_axis(x
            .columns
            .str.lower()
            .str.replace(' ', '_')
            , axis='columns'
        ))    
        .reset_index(drop=True)
        .rename(columns = {
            '#_of_turns' : 'num_turns'
        })
        .loc[:, [
            'date', 'time', 'type', 'player_red', 'player_blue', 'result', 'ending', 'num_turns', 'duration'
        ]]
    )
    results = results.append(update, ignore_index=True)
    pkg.save_dataset(results, 'results')


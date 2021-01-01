#          Copyright Rein Halbersma 2018-2021.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import datetime as dt
import os
import shutil

import pandas as pd
from tqdm import tqdm

import gravon.package as pkg

import scripts.extract.scrape as scrape


def get_daily():
    try:
        last = dt.date(*map(int, sorted(os.listdir(pkg.daily_dir))[-1].split('.')[0].split('-')[1:]))
        results = pkg.load_dataset('results')
        assert last == dt.date(*map(int, results.date.max().split('-')))
        start = last + dt.timedelta(days=1)
    except:
        results = pd.DataFrame()
        start = dt.date(2003, 6, 1)
    filenames = scrape.results(start, pd.to_datetime('today').date(), pkg.daily_dir)
    try:
        update = (pd
            .concat([
                    pd.read_csv(os.path.join(pkg.daily_dir, filename))
                    for filename in tqdm(filenames)
                ],
                ignore_index=True
            )
            .rename(columns=lambda c: c.lower())
            .rename(columns=lambda c: c.replace(' ', '_'))
            .rename(columns={
                '#_of_turns' : 'num_turns'
            })
            .loc[:, [
                'date', 'time', 'type', 'player_red', 'player_blue', 'result', 'ending', 'num_turns', 'duration'
            ]]
        )
    except:
        update = pd.DataFrame()
    if not update.empty:
        results = results.append(update, ignore_index=True)
        pkg.save_dataset(results, 'results')
    return results, update


def remove_daily() -> bool:
    try:
        shutil.rmtree(pkg.daily_dir, ignore_errors=True)
        pkg.remove_dataset('results')
        return True
    except:
        return False


#          Copyright Rein Halbersma 2018-2021.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import datetime as dt
import os

import pandas as pd
from tqdm import tqdm

import gravon.package as pkg
import gravon.transform.label as label
import gravon.transform.tidy as tidy

results = pkg.load_dataset('results')
sr2 = label.results(results)
pkg.save_dataset(sr2, 'sr2')

all_results = (tidy
    .results(raw_results)
    .query('player_red.notnull() & player_blue.notnull()')
)

# There have been 798K matches.
all_results.shape[0]

# There have been almost 70K players.
all_players = tidy.players(all_results)
all_players.player.unique().shape[0]

# There have been over 268K different match-ups (independent of colors).
all_pvsp = tidy.unique_pvsp(all_players)
all_pvsp.shape[0]

# Until 2004-02-25, neither the ending nor the # of turns were recorded in the daily results.
no_ending_turns = all_results.query('ending.isnull() | turns.isnull()')
assert (no_ending_turns.ending.isnull() & no_ending_turns.turns.isnull()).all()
assert no_ending_turns.date.max() == dt.date(2004, 2, 25)

# Until 2004-02-25, there were almost 4K players
players = gr.tidy.players(no_ending_turns)
players.player.unique().shape[0]

# Until 2004-02-25, there were over 15K different match-ups (independent of colors). 
pvsp = tidy.unique_pvsp(players)
pvsp.shape[0]

if cached_pvsp:
    raw_pvsp = gr.datasets.load_dataset('raw_pvsp')
else:
    raw_pvsp = pd.concat([
        gr.scrape.pvsp(r.nick1, r.nick2)
        for _, r in tqdm(pvsp.iterrows(), total=pvsp.shape[0])
    ])
    gr.datasets.save_dataset(raw_pvsp, 'raw_pvsp')
df = (gr.tidy
    .pvsp(raw_pvsp)
    .sort_values(['date', 'time'])
    .reset_index(drop=True)
    .query('date <= "2004-02-25"')
    .reset_index()
    .rename(columns={'index': 'gid'})
)

pre_results = df.query('date < "2003-06-01"')
pre_players = gr.tidy.players(pre_results)
pre_players.player.unique().shape[0]
pre_pvsp = gr.tidy.unique_pvsp(pre_players)
pre_pvsp.shape[0]

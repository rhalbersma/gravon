#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://stratego-tips.blogspot.com/2017/05/best-winning-percentage-stratego-game.html

import pandas as pd

import gravon.package as pkg
import gravon.pattern as pattern

top_setups = {
    'version1': (
        """
        2465276146
        7282229X8B
        25347263BF
        53BBB4353B
        """
    ),
    'version2': (
        """
        2545274146
        7298242X8B
        52362273BF
        35BB6B363B
        """
    ),
}

classic_xml = (pkg
    .load_dataset('ss2')
    .query('type == "classic" & ext == ".xml"')
    .assign(result = lambda r: r.result.cat.reorder_categories(['win', 'loss', 'draw']))
)

for s in top_setups.values():
    df = pattern.equal(classic_xml, s, mirrored=False)
    print(s)
    print("Here's a listing of the game files for the setup above:\n")
    print(pd.crosstab(df.player, df.result, margins=True), '\n')
    for row in df.sort_values('filename').itertuples():
        print(f'{row.player.capitalize():4} {row.result.capitalize():4} {row.filename}') 

classic = (pkg
    .load_dataset('ss2')
    .query('type == "classic"')
)
 
for s in top_setups.values():
    df = pattern.equal(classic, s, mirrored=True)
    print(s)
    print("Here's a listing of the game files for the setup above:\n")
    print(pd.crosstab([df.player, df.match_type], df.result, margins=True), '\n')
    print(pd.crosstab(df.period, df.result, margins=True), '\n')
    for row in df.itertuples():
        print(f'{row.player.capitalize():4} {row.result.capitalize():4} {row.filename}') 

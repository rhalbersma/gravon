#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# http://stratego-tips.blogspot.com/2017/12/marshal-blitzer-games-from-gravon.html

import pandas as pd

import gravon.package as pkg
import gravon.pattern as pattern

blitz = (
    """
    62572264B2
    8X715986B5
    232B325742
    64BFB334B3
    """
)

classic_xml = (pkg
    .load_dataset('ss2')
    .query('type == "classic" & ext == ".xml"')
    .assign(result = lambda r: r.result.cat.reorder_categories(['win', 'loss', 'draw']))
)

df = pattern.equal(classic_xml, blitz, mirrored=False)
print(blitz)
print("Here's a listing of the game files for the setup above:\n")
print(pd.crosstab(df.player, df.result, margins=True), '\n')
for row in df.sort_values('filename').itertuples():
    print(f'{row.player.capitalize():4} {row.result.capitalize():4} {row.filename}') 

classic = (pkg
    .load_dataset('ss2')
    .query('type == "classic"')
)
 
df = pattern.equal(classic, blitz, mirrored=True)
print(blitz)
print("Here's a listing of the game files for the setup above:\n")
print(pd.crosstab([df.player, df.match_type], df.result, margins=True), '\n')
print(pd.crosstab(df.period, df.result, margins=True), '\n')
for row in df.itertuples():
    print(f'{row.player.capitalize():4} {row.result.capitalize():4} {row.filename}') 

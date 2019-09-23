#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import pandas as pd

import gravon.strados2
import gravon.utils
import gravon.wget

def init_bekenden(downloads_dir='downloads/bekenden', games_dir='games/bekenden') -> pd.DataFrame:
    gravon.wget.download(downloads_dir, 'http://members.chello.nl/~l.adriaansen/Bekenden.zip')
    gravon.utils.extract(downloads_dir, '*.zip', games_dir)
    gravon.utils.flatten(games_dir)
    df = gravon.strados2.to_frame(games_dir, '*.gsn', lambda x: gravon.strados2.gsn_parser(x, date_id=False))
    df = df.astype(dtype={column: 'category' for column in ['game_type', 'result_type', 'result_winner']})
    df = df.iloc[df.filename.str.lower().argsort()]
    df.reset_index(drop=True, inplace=True)
    return df

def main():
    bekenden = init_bekenden()
    bekenden.drop(columns=['game_type', 'date', 'id'], inplace=True)
    bekenden.rename(columns={'filename': 'bestandsnaam'}, inplace=True)
    games = gravon.load_dataset('games')
    games.query('game_type == "classic"', inplace=True)
    games.drop(columns=['game_type', 'player_id1', 'player_id2'], inplace=True)
    matches = games.merge(bekenden)

#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import gravon.wget as wget

wget.mirror_no_directories('games/zip', '*.zip', 'http://www.gravon.de/strados2/files/')
wget.download('games/player', 'https://www.gravon.de/webstart/strados2/strados2.jnlp')

import gravon.piece
import gravon.setup
import gravon.strados2
import gravon.utils
import gravon.wget

def init_games(downloads_dir='downloads/gravon', games_dir='games/gravon') -> pd.DataFrame:
    #gravon.wget.mirror_no_directories(downloads_dir, '*.zip', 'http://www.gravon.de/strados2/files/')
    gravon.utils.extract(downloads_dir, '*.zip', games_dir)
    gravon.utils.flatten(games_dir)
    df = pd.concat([
        gravon.strados2.to_frame(games_dir, '*.gsn', gravon.strados2.gsn_parser),
        gravon.strados2.to_frame(games_dir, '*.xml', gravon.strados2.xml_parser)
    ])
    df = df.astype(dtype={column: 'category' for column in ['game_type', 'result_type', 'result_winner']})
    df.sort_values(by=['game_type', 'date', 'id'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def init_setups(df: pd.DataFrame) -> pd.DataFrame:
    df.query('game_type != "free" & field_content.str.len() == 100', inplace=True)
    df['setup_tuple'] = df['field_content'].apply(lambda x: gravon.strados2.split(x))
    df[['setup1', 'setup2']] = pd.DataFrame(df['setup_tuple'].values.tolist(), index=df.index)
    df.drop(columns=['field_content', 'setup_tuple'], inplace=True)
    df = pd.wide_to_long(df, ['player_id', 'setup'], i='filename', j='player')
    df.reset_index(inplace=True)
    df.rename(columns={'setup': 'strados2'}, inplace=True)
    df = df.astype(dtype={column: 'category' for column in ['player']})
    df.sort_values(by=['game_type', 'date', 'id', 'player'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['setup_EU'] = df['strados2'].apply(lambda x: gravon.strados2.encode(x, piece.symbols['EU']))
    df['setup_US'] = df['strados2'].apply(lambda x: gravon.strados2.encode(x, piece.symbols['US']))
    return df

def main():
    games = init_games()
    gravon.utils.save_dataset(games, 'games')

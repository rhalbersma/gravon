#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import collections
import glob
import itertools
import os
import pkg_resources
import shutil
import zipfile

import bs4
import lxml.etree
import pandas as pd
import requests

class Wget:
    def mirror_no_directories(prefix: str, acclist: str, *urls) -> None:
        """
        wget -m -nd -P prefix -A acclist urls

        Examples:
            >>> Wget.mirror_no_directories('downloads', '*.zip', 'http://www.gravon.de/strados2/files/')
        """
        os.makedirs(prefix, exist_ok=True)
        urls = collections.deque(urls)
        while urls:
            top = urls.popleft()
            response = requests.get(top)
            assert response.status_code == 200
            soup = bs4.BeautifulSoup(response.content, 'lxml')
            for link in soup.find_all('a'):
                filename = link.get('href')
                if filename.endswith('/') and not filename.startswith('/'):
                    urls.append(top + filename)
                    continue
                if not filename.endswith(acclist.split('.')[-1]):
                    continue
                response = requests.get(os.path.join(top, filename))
                assert response.status_code == 200
                with open(os.path.join(prefix, filename), 'wb') as dst:
                    dst.write(response.content)

    def download(prefix: str, *urls) -> None:
        """
        wget -P prefix urls

        Examples:
            >>> Wget.download('viewer', 'https://www.gravon.de/webstart/strados2/strados2.jnlp')
        """
        os.makedirs(prefix, exist_ok=True)
        for url in urls:
            response = requests.get(url)
            assert response.status_code == 200
            filename = url.split('/')[-1]
            with open(os.path.join(prefix, filename), 'wb') as dst:
                dst.write(response.content)

def extract(name: str, pattern: str, path: str) -> None:
    """
    Examples:
        >>> extract('downloads', '*.zip', 'games')
    """
    assert os.path.isdir(name)
    os.makedirs(path, exist_ok=True)
    for f in glob.glob(os.path.join(name, pattern)):
        with zipfile.ZipFile(f) as src:
            src.extractall(path)

def flatten(path: str) -> None:
    """
    Examples:
        >>> flatten('games')
    """
    assert os.path.isdir(path)
    for dirpath, dirnames, filenames in itertools.islice(os.walk(path), 1, None):
        for f in filenames:
            shutil.move(os.path.join(dirpath, f), os.path.join(path, f))
    for dirpath, dirnames, filenames in os.walk(path):
        for d in dirnames:
            nested = os.path.join(dirpath, d)
            assert not os.listdir(nested)
            shutil.rmtree(nested)
    assert all([ os.path.isfile(os.path.join(path, f)) for f in os.listdir(path) ])

def gsn_parser(path: str) -> tuple:
    filename = os.path.basename(path)    
    root = os.path.splitext(filename)[0].split('.')[1:]
    date, id = '.'.join(root[:-1]), int(root[-1])
    with open(path, 'r') as src:
        # header opening
        line = src.readline().strip()
        assert line[:-1] == '#X38FA11 Stratego-Notation v'
        assert int(line[-1]) in range(1, 3)

        # game type
        line = src.readline().strip()
        assert line.startswith('type')
        game_type = {
            0: 'classic',
            1: 'barrage',
            2: 'free',
            3: 'ultimate'
        }[int(line[-1])]

        # field content
        last_line = src.tell()
        line = src.readline().strip()
        if line == 'END':
            # undo reading the current line if the game ended before the setup phase had been completed
            src.seek(last_line)
            field_content = ''
        else:
            assert len(line) == 100
            field_content = line

        # moves
        moves = 0
        while True:
            line = src.readline().strip()
            if line == 'END':
                break
            assert len(line) == 5
            if line[2] == ':':
                # bug report pending for rescue moves in Ultimate Lightning (private communication on 2019-06-16)
                continue
            moves += 1

        # players and result
        line = src.readline().strip()
        players, result = line.split(' result ')
        player_id1, player_id2 = players.split(' vs ')
        result_type, result_winner = (int(r) for r in result.split(' winner '))
        result_winner += 1

    return filename, game_type, date, id, field_content, moves, player_id1, player_id2, result_type, result_winner

def xml_parser(path: str) -> tuple:
    assert os.path.isfile(path)
    tree = lxml.etree.parse(path)
    filename = os.path.basename(path)    
    root = os.path.splitext(filename)[0].split('-')[1:]
    date, id = root[0], int(root[1])
    game_type = {
        'classic'           : 'classic',
        'barrage'           : 'barrage',
        'classicfree'       : 'free',
        'ultimate lightning': 'ultimate',
        'duell'             : 'duel'
    }[tree.find('.//game').attrib['type']]
    field = tree.find('.//field')
    field_content = '' if field == None else field.attrib['content']
    moves = len(tree.findall('.//move'))
    player_id1, player_id2 = (p.text for p in tree.findall('.//player'))
    result = tree.find('.//result')
    result_type, result_winner = (int(r) for r in (result.attrib['type'], result.attrib['winner']))
    return filename, game_type, date, id, field_content, moves, player_id1, player_id2, result_type, result_winner

def to_frame(path: str, pattern: str, parser) -> pd.DataFrame:
    assert os.path.isdir(path)
    return pd.DataFrame(
        data=[parser(file) for file in glob.glob(os.path.join(path, pattern))],
        columns=['filename', 'game_type', 'date', 'id', 'field_content', 'moves', 'player_id1', 'player_id2', 'result_type', 'result_winner']
    )

def init_datasets(downloads_dir: str='downloads', games_dir: str='games') -> pd.DataFrame:
    Wget.mirror_no_directories(downloads_dir, '*.zip', 'http://www.gravon.de/strados2/files/')
    extract(downloads_dir, '*.zip', games_dir)
    flatten(games_dir)
    df = pd.concat([
        to_frame(games_dir, '*.gsn', gsn_parser),
        to_frame(games_dir, '*.xml', xml_parser)
    ])
    df = df.astype(dtype={column: 'category' for column in ['game_type', 'result_type', 'result_winner']})
    df.sort_values(by=['game_type', 'date', 'id'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def get_resource(basename: str) -> str:
    return pkg_resources.resource_filename(__name__, os.path.join('data', basename))

def save_dataset(df: pd.DataFrame, name: str) -> None:
    df.to_pickle(get_resource(name + '.pkl'))

def load_dataset(name: str) -> pd.DataFrame:
    return pd.read_pickle(get_resource(name + '.pkl'))

def download_daily_results(year, month, day) -> pd.DataFrame:
    url = f'http://www.gravon.de/gravon/stratego/todays.jsp?year={year}&month={month}&day={day}'
    response = requests.get(url)
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    table = soup.find_all('table', {'width': '95%', 'align': 'center'})[1]
    df = pd.read_html(str(table), header=0)[0]
    df.columns = df.columns.str.replace(' ', '_')
    return df

def download_monthly_results(year, month) -> pd.DataFrame:
    return pd.concat([ download_daily_results(year, month, day) for day in range(1, 29) ])

def download_kleier_tournament(eid: int) -> pd.DataFrame:
    url = f'https://www.kleier.net/cgi/tourn_table.php?eid={eid}'
    response = requests.get(url)
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    tables = soup.find_all('table')
    return [ pd.read_html(str(table))[0].head(-1) for table in tables ]

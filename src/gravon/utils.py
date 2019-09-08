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
    def mirror_no_directories(acclist: str, prefix: str, *urls) -> None:
        """
        wget -m -nd -A acclist -P prefix urls

        Examples:
            >>> gravon.utils.Wget.mirror_no_directories('*.zip', 'downloads', 'http://www.gravon.de/strados2/files/')
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
            >>> gravon.utils.Wget.download('viewer', 'https://www.gravon.de/webstart/strados2/strados2.jnlp')
        """
        os.makedirs(prefix, exist_ok=True)
        for url in urls:
            response = requests.get(url)
            assert response.status_code == 200
            filename = url.split('/')[-1]
            with open(os.path.join(prefix, filename), 'wb') as dst:
                dst.write(response.content)

def extract(pattern: str, name: str, path: str) -> None:
    """
    Examples:
        >>> gravon.utils.extract('*.zip', 'downloads', 'games')
    """
    assert os.path.isdir(name)
    os.makedirs(path, exist_ok=True)
    for f in glob.glob(os.path.join(name, pattern)):
        with zipfile.ZipFile(f) as r:
            r.extractall(path)

def flatten(path: str) -> None:
    """
    Examples:
        >>> gravon.utils.flatten('games')
    """
    for dirpath, dirnames, filenames in itertools.islice(os.walk(path), 1, None):
        for f in filenames:
            shutil.move(os.path.join(dirpath, f), os.path.join(path, f))
    for dirpath, dirnames, filenames in os.walk(path):
        for d in dirnames:
            nested = os.path.join(dirpath, d)
            assert not os.listdir(nested)
            shutil.rmtree(nested)

def replace(path: str, old: str, new: str) -> None:
    """
    Examples:
        >>> gravon.utils.replace('games', ' ', '_')
    """
    for f in os.listdir(path):
        src = os.path.join(path, f)
        os.rename(src, src.replace(old, new))

def tableofcontents(path: str) -> pd.DataFrame:
    toc = pd.DataFrame(
        data=[ 
            os.path.splitext(os.path.basename(f))
            for f in glob.glob(os.path.join(path, '*'))
        ], 
        columns=['game_id', 'game_fmt']
    )
    toc['game_fmt'] = toc['game_fmt'].astype('category')
    return toc

class GSNParser:
    def xml_game_type(gsn_game_type: int) -> str:
        return {
            0: 'classic',
            1: 'barrage',
            2: 'classicfree',
            3: 'ultimate lightning'
        }.get(gsn_game_type, gsn_game_type)

    def parse(self, path) -> None:
        root = os.path.splitext(path)[0]
        with open(root + '.gsn', 'r') as src, open(root + '.xml', 'w') as dst:
            # header opening
            line = src.readline().strip()
            assert line[:-1] == '#X38FA11 Stratego-Notation v'
            assert int(line[-1]) in range(1, 3)
            print('<?xml version="1.0" encoding="UTF-8"?>', file=dst)
            print('<stratego>', file=dst)

            # game type
            line = src.readline().strip()
            assert line.startswith('type')
            gsn_game_type = int(line[-1])
            assert gsn_game_type in range(4)
            print(' <game type = "{}">'.format(xml_game_type(gsn_game_type)), file=dst)
            print(file=dst)

            # field content
            last_line = src.tell()
            line = src.readline().strip()
            if line == 'END':
                # undo reading the current line if the game ended before the setup phase had been completed
                src.seek(last_line)
            else:
                assert len(line) == 100
                print('  <field content="{}"/>'.format(line), file=dst)

            # moves
            id = 0
            while True:
                line = src.readline().strip()
                if line == 'END':
                    break
                assert len(line) == 5
                if line[2] == ':':
                    # bug report pending for rescue moves in Ultimate Lightning (private communication on 2019-06-16)
                    continue
                id += 1
                source, target = line.split('-')
                print('  <move id="{}" source="{}" target="{}"/>'.format(id, source, target), file=dst)

            # result
            line = src.readline().strip()
            players, result = line.split(' result ')
            player1, player2 = players.split(' vs ')
            type, winner = result.split(' winner ')
            print('  <player id ="1">{}</player>'.format(player1), file=dst)
            print('  <player id ="2">{}</player>'.format(player2), file=dst)
            print('  <result type="{}" winner="{}"/>'.format(type, int(winner) + 1), file=dst)

            # header closing
            print(' </game>', file=dst)
            print('</stratego>', file=dst)

    def __call__(self, sources):
        for src in sources:
            gsn2xml(src)
            os.remove(src)

def xml_parse(path: str) -> tuple:
    tree = lxml.etree.parse(path)
    game_id = os.path.splitext(os.path.basename(path))[0]
    game_type = tree.find('.//game').attrib['type'] if not game_id.startswith('duell-') else 'duell'
    field = tree.find('.//field')
    field_content = '' if field == None else field.attrib['content']
    game_length = len(tree.findall('.//move'))
    name1, name2 = (p.text for p in tree.findall('.//player'))
    result = tree.find('.//result')
    result_type, winner = map(int, (result.attrib['type'], result.attrib['winner']))
    return game_id, game_type, field_content, game_length, name1, name2, result_type, winner

def create_dataset(pattern: str, path: str, toc: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    data=[
        xml_parse(f) 
        for f in glob.glob(os.path.join(path, pattern))
    ] 
    df = pd.DataFrame(
        data,
        columns=['game_id', 'game_type', 'field_content', 'game_length', 'name1', 'name2', 'result_type', 'winner']
    )
    df = df.astype(dtype={ column: 'category' for column in ['game_type', 'result_type', 'winner'] })
    empty = df.query('field_content.str.len() != 100')
    df.query('field_content.str.len() == 100', inplace=True)
    df = toc.merge(df)
    if empty.shape[0]:
        empty = toc.merge(empty)
    return df, empty

def init_datasets(downloads_dir: str='downloads', games_dir: str='games') -> pd.DataFrame:
    #Wget.mirror_no_directories('*.zip', downloads_dir, 'http://www.gravon.de/strados2/files/')
    extract('*.zip', downloads_dir, games_dir)
    flatten(games_dir)
    replace(games_dir, ' ', '_')
    toc = tableofcontents(games_dir)
    #GSNParser()(glob.glob(os.path.join(games_dir, '*.gsn')))
    df = create_dataset('*.xml', games_dir, toc)
    return df

def save_dataset(path: str) -> None:
    pd.to_pickle(path)

def load_dataset(name: str) -> pd.DataFrame:
    path = pkg_resources.resource_filename('gravon', os.path.join('data', name + '.pkl'))
    return pd.read_pickle(path)

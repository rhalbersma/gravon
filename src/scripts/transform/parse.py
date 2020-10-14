#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os.path as osp
from typing import Callable, Iterable, Optional, Tuple

import lxml.etree
import pandas as pd
from tqdm import tqdm

import gravon.package as pkg

GameHeader = Tuple[int, int, str, str, int, int, int, Optional[str]]
GameBody   = pd.DataFrame

def _gsn(gid: int, filename: str) -> Tuple[GameHeader, GameBody]:
    path = osp.join(pkg.txt_dir, filename)
    with open(path, 'r', encoding='utf-8-sig') as src:
        lines = src.read().splitlines()
        assert lines[0][:-1] == '#X38FA11 Stratego-Notation v'
        assert int(lines[0][-1]) in range(1, 3)

        assert lines[1].startswith('type')
        type = int(lines[1][-1])

        assert lines[-2] == 'END'
        field_content = lines[2] if lines[2:-2] else None

        game_body = pd.DataFrame(
            data=[ 
                (gid, mid, line[:2], line[3:]) 
                for mid, line in enumerate(lines[3:-2])
                if line[2] != ':'
            ],
            columns=[ 
                'gid', 'mid', 'source', 'target' 
            ],
            dtype=int
        )
        num_moves = game_body.shape[0]

        players, result = lines[-1].split(' result ')
        player_red, player_blue = players.split(' vs ')
        ending, result = (
            int(attrib) for 
            attrib in result.split(' winner ')
        )

    return (gid, type, player_red, player_blue, result, ending, num_moves, field_content), game_body

def _xml(gid: int, filename: str) -> Tuple[GameHeader, GameBody]:
    path = osp.join(pkg.txt_dir, filename)
    tree = lxml.etree.parse(path)

    type = {
        'classic'           : 0,
        'barrage'           : 1,
        'classicfree'       : 2,
        'ultimate lightning': 3,
        'duell'             : 4
    }[tree.find('//game').attrib['type']]

    try:
        field_content = tree.find('//field').attrib['content']
    except:
        field_content = None
    
    game_body = pd.DataFrame(
        data=[ 
            (gid, mid, move.attrib['source'], move.attrib['target']) 
            for mid, move in enumerate(tree.findall('//move'))
        ],
        columns=[
            'gid', 'mid', 'source', 'target'
        ],
        dtype=int
    )
    num_moves = game_body.shape[0]
    
    player_red, player_blue = (
        p.text 
        for p in tree.findall('//player')
    )
    
    result, ending = (
        int(tree.find('//result').attrib[a])
        for a in ('winner', 'type')
    )
    result -= 1
    
    return (gid, type, player_red, player_blue, result, ending, num_moves, field_content), game_body

def _concatter(index: Iterable[GameHeader], games: Iterable[GameBody]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return pd.DataFrame(
        data=index, 
        columns=[
            'gid', 'type', 'player_red', 'player_blue', 'result', 'ending', 'num_moves', 'field_content'
        ]
    ), pd.concat(games)

def _selection(files: pd.DataFrame, parser: Callable[[int, str], Tuple[GameHeader, GameBody]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return _concatter(*zip(*[
        parser(row.gid, row.filename)
        for row in tqdm(files.itertuples(), total=files.shape[0])
    ]))

def index_games(files: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    index, games = (
        pd.concat(list(t), sort=False, ignore_index=True)
        for t in zip(*[
            _selection(files.query('ext == @ext'), parser)
            for ext, parser in [
                ('.gsn', _gsn),
                ('.xml', _xml)
            ]
        ])
    )
    return index, games

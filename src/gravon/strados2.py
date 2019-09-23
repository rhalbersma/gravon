#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# page 90 of Vincent de Boer's MSc. thesis:
# http://www.kbs.twi.tudelft.nl/docs/MSc/2007/deBoer/thesis.pdf

import glob
import os

import lxml.etree
import pandas as pd

symbols = \
    [ 'M' ] + [ chr(i) for i in range(ord('B') + 1, ord('M')) ] + [ 'B' ] + \
    [ 'A', '_' ] + \
    [ 'Y' ] + [ chr(i) for i in range(ord('N') + 1, ord('Y')) ] + [ 'N' ]

ranks = { 
    symbol : rank
    for rank, symbol in enumerate(symbols) 
}

def split(field_content: str) -> (str, str):
    """Split a 100-character field content string into a tuple of two 40-character setup strings."""
    assert len(field_content) == 100
    return field_content[:40], field_content[60:][::-1]

def parse(setup: str) -> list:
    """Parse a string of symbols into a list of ranks."""
    return [
        ranks[symbol]
        for symbol in setup
    ]

def generate(placement: list) -> str:
    """Generate a string of symbols from a list of ranks."""
    return ''.join([
        symbols[rank]
        for rank in placement
    ])

def encode(setup: str, encoding: list) -> str:
    """Encode a string of symbols."""
    return ''.join([
        encoding[rank]
        for rank in parse(setup)
    ])

def gsn_parser(path: str, date_id=True) -> tuple:
    filename = os.path.basename(path)
    date = id = None
    if date_id:
        root = os.path.splitext(filename)[0].split('.')[1:]
        assert len(root[:-1]) == 3
        date = '-'.join(root[:-1])
        id = int(root[-1])
    with open(path, 'r', encoding='utf-8-sig') as src:
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

def xml_parser(path: str, date_id=True) -> tuple:
    assert os.path.isfile(path)
    tree = lxml.etree.parse(path)
    filename = os.path.basename(path)
    date = id = None
    if date_id:
        root = os.path.splitext(filename)[0].split('-')[1:]
        year, month = (int(t) for t in root[0].split('.'))
        if month == 0:
            year -= 1
            month = 12
        date = '-'.join([str(year), str(month).zfill(2)])
        id = int(root[1])
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

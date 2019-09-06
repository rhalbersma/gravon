#!/usr/bin/env python

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import glob
import os
import sys

import lxml.etree
import pandas as pd

def xml2tuple(path):
    tree = lxml.etree.parse(path)
    game_id = os.path.splitext(os.path.basename(path))[0]
    game_type = tree.find('.//game').attrib['type'] if not game_id.startswith('duell-') else 'duell'
    field = tree.find('.//field')
    field_content = '' if field == None else field.attrib['content']
    game_length = len(tree.findall('.//move'))
    name1, name2 = (p.text for p in tree.findall('.//player'))
    result = tree.find('.//result')
    result_type, winner = result.attrib['type'], result.attrib['winner']
    return (game_id, game_type, field_content, game_length, name1, name2, result_type, winner)

def xml2csv(dest, sources):
    data = []
    for src in sources:
        data.append(xml2tuple(src))
    df = pd.DataFrame(data, columns=['game_id', 'game_type', 'field_content', 'game_length', 'name1', 'name2', 'result_type', 'winner'])
    empty = df.query('field_content.str.len() != 100')
    df.query('field_content.str.len() == 100', inplace=True)
    toc = pd.read_csv('data/toc.csv')
    df = toc.merge(df)
    df.to_csv(dest, index=False)
    if empty.shape[0]:
        empty = toc.merge(empty)
        root, ext = os.path.splitext(dest)
        empty.to_csv(root + '-empty' + ext, index=False)

def main():
    os.makedirs('data', exist_ok=True)
    xml2csv('data/barrage.csv',  glob.glob('games/barrage*.xml'))
    xml2csv('data/classic.csv',  glob.glob('games/classic[.-]*.xml'))
    xml2csv('data/duell.csv',    glob.glob('games/duell*.xml'))
    xml2csv('data/free.csv',     glob.glob('games/*free*.xml'))
    xml2csv('data/ultimate.csv', glob.glob('games/ultimate*.xml'))

if __name__== '__main__':
    sys.exit(main())

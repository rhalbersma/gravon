#!/usr/bin/env python3

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import sys

import lxml.etree
import pandas as pd

def xml2tuple(path):
    tree = lxml.etree.parse(path)
    game_id = os.path.basename(path)
    game_type = tree.find('.//game').attrib['type'] if not game_id.startswith('duell-') else 'duell'
    field = tree.find('.//field')
    field_content = '' if field == None else field.attrib['content']
    game_length = len(tree.findall('.//move'))
    name1, name2 = (p.text for p in tree.findall('.//player'))
    result = tree.find('.//result')
    result_type, winner = result.attrib['type'], result.attrib['winner']
    return (game_id, game_type, field_content, game_length, name1, name2, result_type, winner)

def main(args):
    data = []
    xml_files = (a for a in args[1:] if a.endswith('.xml'))
    for a in xml_files:
        data.append(xml2tuple(a))
    df = pd.DataFrame(data, columns=['game_id', 'game_type', 'field_content', 'game_length', 'name1', 'name2', 'result_type', 'winner'])
    empty = df.query('field_content.str.len() != 100')
    df.query('field_content.str.len() == 100', inplace=True)
    df.to_csv(args[0], index=False)
    if empty.shape[0]:
        root, ext = os.path.splitext(argv[0])
        empty.to_csv(root + '-empty' + ext, index=False)
    pass

if __name__== '__main__':
    main(sys.argv[1:])

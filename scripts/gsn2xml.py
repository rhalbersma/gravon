#!/usr/bin/env python3

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os
import sys

def game_type(n):
    return {
        0: 'classic',
        1: 'barrage',
        2: 'classicfree',
        3: 'ultimate lightning'
    }[n]

def gsn2xml(path):
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
        type = int(line[-1])
        assert type in range(4)
        print(' <game type = "%s">' % game_type(type), file=dst)
        print(file=dst)

        # field content
        last_line = src.tell()
        line = src.readline().strip()
        if line == 'END':
            # undo reading the current line if the game ended before the setup phase had been completed
            src.seek(last_line)
        else:
            assert len(line) == 100
            print('  <field content="%s"/>' % line, file=dst)

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
            print('  <move id="%d" source="%s" target="%s"/>' % (id, source, target), file=dst)

        # result
        line = src.readline().strip()
        players, result = line.split(' result ')
        player1, player2 = players.split(' vs ')
        type, winner = result.split(' winner ')
        print('  <player id ="1">%s</player>' % player1, file=dst)
        print('  <player id ="2">%s</player>' % player2, file=dst)
        print('  <result type="%s" winner="%d"/>' % (type, int(winner) + 1), file=dst)

        # header closing
        print(' </game>', file=dst)
        print('</stratego>', file=dst)

def main(args):
    gsn_files = (a for a in args if a.endswith('.gsn'))
    for a in gsn_files:
        gsn2xml(a)
        os.remove(a)
    pass

if __name__== '__main__':
    main(sys.argv[1:])

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

names = [ 'flag', 'spy', 'scout', 'miner', 'sergeant', 'lieutenant', 'captain', 'major', 'colonel', 'general', 'marshal', 'bomb' ]

def chars(piece_fmt: str='EU') -> list:
    switch = {
        'EU' : [ 'F' ] + [ str(i) for i in range(1, 10) ] + [ 'X', 'B' ],
        'US' : [ 'F', 'S' ] + [ str(i) for i in reversed(range(1, 10)) ] + [ 'B' ]
    }
    return switch.get(piece_fmt, piece_fmt)

def ranks(piece_fmt: str='EU') -> list:
    switch = { fmt : dict(zip(chars(piece_fmt), range(12))) for fmt in [ 'EU', 'US' ] }
    return switch.get(piece_fmt, piece_fmt)

def translate(piece_char: str, src_fmt: str='EU', dst_fmt: str='US') -> str:
    assert len(piece_char) == 1
    switch = dict(zip(chars(src_fmt), chars(dst_fmt)))
    return switch.get(piece_char, piece_char)

# flag, spy, general and marshal
unique_ranks = [ 0, 1, 9, 10 ]

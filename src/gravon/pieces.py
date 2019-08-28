#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

names = [ 'flag', 'spy', 'scout', 'miner', 'sergeant', 'lieutenant', 'captain', 'major', 'colonel', 'general', 'marshal', 'bomb' ]

chars = {
    'EU' : [ 'F' ] + [ str(i) for i in range(1, 10) ] + [ 'X', 'B' ],
    'US' : [ 'F', 'S' ] + [ str(i) for i in reversed(range(1, 10)) ] + [ 'B' ]
}

ranks = { fmt : dict(zip(chars[fmt], range(12)))  for fmt in [ 'EU', 'US' ] }

switch_EU2US = dict(zip(chars['EU'], chars['US']))
switch_US2EU = dict(zip(chars['US'], chars['EU']))

def EU2US(piece: str) -> str:    
    return switch_EU2US.get(piece, piece)

def US2EU(piece: str) -> str:
    return switch_US2EU.get(piece, piece)

unique_ranks = [ 0, 1, 9, 10 ]

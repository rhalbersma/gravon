#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

names = [
    'flag', 'spy', 'scout', 'miner', 'sergeant', 'lieutenant', 'captain',
    'major', 'colonel', 'general', 'marshal', 'bomb', 'empty', 'lake'
]

nrank = len(names)

symbols = {
    'EU': [ 'F', '1' ] + [ str(rank) for rank in          range(2, 10)  ] + [ 'X', 'B' ] + [ '.', '#' ],
    'US': [ 'F', 'S' ] + [ str(rank) for rank in reversed(range(2, 10)) ] + [ '1', 'B' ] + [ '.', '#' ]
}

ranks = {
    notation: { 
        symbol: rank 
        for rank, symbol in enumerate(symbols[notation]) 
    }
    for notation in symbols.keys()
}

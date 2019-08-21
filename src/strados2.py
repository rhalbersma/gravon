#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

class SetupParser:
    # page 90 of Vincent de Boer's thesis
    # http://www.kbs.twi.tudelft.nl/docs/MSc/2007/deBoer/thesis.pdf
    pieces_R = ['M'] + [ chr(i) for i in range(ord('B') + 1, ord('M')) ] + ['B']
    pieces_B = ['Y'] + [ chr(i) for i in range(ord('N') + 1, ord('Y')) ] + ['N']

    def __init__(self, encoding: list):
        self.decode = {
            **{ self.pieces_R[rank] : piece for rank, piece in enumerate(encoding) },
            **{ self.pieces_B[rank] : piece for rank, piece in enumerate(encoding) }
        }

    def __call__(self, setup: str, player: str) -> str:
        if player == 'B':
            setup = setup[::-1]
        return ''.join([self.decode[piece] for piece in setup])

#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

class Encode:
    # Our notation: 'F' for flag, '1'-'9' for spy-general, 'X' for marshal, and 'B' for bomb.
    pieces = [ 'F' ] + [ str(i) for i in range(1, 10) ] + [ 'X', 'B' ]

    # The number of pieces in a setup
    classic = [ 1, 1, 8, 5, 4, 4, 4, 3, 2, 1, 1, 6 ]
    barrage = [ 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1 ]

class Decode:
    def __init__(self, encoding=Encode()):
        # page 90 of Vincent de Boer's thesis
        # http://www.kbs.twi.tudelft.nl/docs/MSc/2007/deBoer/thesis.pdf
        self.pieces_R = ['M'] + [ chr(i) for i in range(ord('B') + 1, ord('M')) ] + ['B']
        self.pieces_B = ['Y'] + [ chr(i) for i in range(ord('N') + 1, ord('Y')) ] + ['N']

        # A dictionary mapping the StraDoS2 encoding to our conventions.
        self.decoding = {
            **{ '_' : '*', 'A' : '.' },
            **{ self.pieces_R[i] : p for i, p in enumerate(encoding.pieces) },
            **{ self.pieces_B[i] : p for i, p in enumerate(encoding.pieces) }
        }

    def __call__(self, s: str):
        return ''.join([self.decoding[c] for c in s])

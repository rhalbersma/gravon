#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

class SetupParser:
    # page 90 of Vincent de Boer's thesis
    # http://www.kbs.twi.tudelft.nl/docs/MSc/2007/deBoer/thesis.pdf
    pieces_R = ['M'] + [ chr(i) for i in range(ord('B') + 1, ord('M')) ] + ['B']
    pieces_B = ['Y'] + [ chr(i) for i in range(ord('N') + 1, ord('Y')) ] + ['N']

    def __init__(self, encoding: list) -> None:
        self.decode = {
            **{ self.pieces_R[rank] : piece for rank, piece in enumerate(encoding) },
            **{ self.pieces_B[rank] : piece for rank, piece in enumerate(encoding) }
        }

    def __call__(self, field_content: str) -> (str, str):
        setup_R = self.parse(field_content[:40]      )
        setup_B = self.parse(field_content[60:][::-1])
        return setup_R, setup_B

    def parse(self, setup: str) -> str:
        return ''.join([ self.decode[piece] for piece in setup ])

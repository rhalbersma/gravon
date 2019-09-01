#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

class SetupParser:
    def __init__(self, encoding: list) -> None:
        """
        page 90 of Vincent de Boer's MSc. thesis:
        http://www.kbs.twi.tudelft.nl/docs/MSc/2007/deBoer/thesis.pdf
        """
        self.pieces = {
            'R' : ['M'] + [ chr(i) for i in range(ord('B') + 1, ord('M')) ] + ['B'],
            'B' : ['Y'] + [ chr(i) for i in range(ord('N') + 1, ord('Y')) ] + ['N']
        }

        self.decode = {
            **{ self.pieces['R'][rank] : piece for rank, piece in enumerate(encoding) },
            **{ self.pieces['B'][rank] : piece for rank, piece in enumerate(encoding) }
        }

    def __call__(self, field_content: str) -> (str, str):
        """Reads a 100-character field content string and returns a tuple of two parsed 40-character setup strings."""
        assert len(field_content) == 100
        setup_R = self.parse(field_content[:40]      )
        setup_B = self.parse(field_content[60:][::-1])
        return setup_R, setup_B

    def parse(self, setup: str) -> str:
        """Parses a 40-character setup string."""
        assert len(setup) == 40
        return ''.join([ self.decode[piece] for piece in setup ])

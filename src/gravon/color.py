#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from enum import IntEnum

class Color(IntEnum):
    red   = 0,
    blue  = 1,
    Empty = 2,
    Lake  = 3,

color_labels = [
    Color(c).name[0]
    for c in Color
]

#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from enum import IntEnum

class Info(IntEnum):
    unknown = 0,
    moved   = 1,
    known   = 2,
    Empty   = 3,
    Lake    = 4,

info_labels = [
    Info(i).name[0]
    for i in Info
]

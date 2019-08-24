#          Copyright Rein Halbersma 2018-2019.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import math
import scipy.stats

def tpr(n, p, r=0):
    if 0.0 < p < 1.0:
        q = p
        f = 1.0
    else:
        q = (n * p + .5) / (n + 1)
        f = (n + 1) / n
    return f * scipy.stats.norm.ppf(q, loc=r, scale=200 * math.sqrt(2))

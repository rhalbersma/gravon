#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os

import gravon.package as pkg

import scripts.extract.scrape as scrape

def get_player() -> bool:
    if not os.path.exists(pkg.games_dir) or 'strados2.jnlp' not in os.listdir(pkg.games_dir):
        scrape.download(pkg.games_dir, pkg.player_url)
        return True
    return False

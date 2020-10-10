#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import gravon.package          as pkg
import gravon.transform.repair as repair
import gravon.transform.parse  as parse
import gravon.transform.label  as label

txt_files = pkg.load_dataset('txt_files')

if 'repaired' in pkg.get_dataset_names():
    repaired = pkg.load_dataset('repaired')
else:
    repaired = repair.directory(txt_files)
    pkg.save_dataset(repaired, 'repaired')

if all((df in pkg.get_dataset_names() for df in ('parsed_index', 'parsed_games'))):
    parsed_index = pkg.load_dataset('parsed_index')
    parsed_games = pkg.load_dataset('parsed_games')
else:
    parsed_index, parsed_games = parse.index_games(txt_files)
    pkg.save_dataset(parsed_index, 'parsed_index')
    pkg.save_dataset(parsed_games, 'parsed_games')

si2 = label.index(txt_files.merge(parsed_index, on=['gid', 'type'], validate='one_to_one'))
sg2 = label.games(parsed_games)
pkg.save_dataset(si2, 'si2')
pkg.save_dataset(sg2, 'sg2')

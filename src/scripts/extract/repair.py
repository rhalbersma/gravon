#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import os.path as osp
from typing import Callable, List, Tuple

import lxml.etree
import pandas as pd
from tqdm import tqdm
from typing import Optional

def _gsn(dirname: str, basename: str) -> Tuple[Optional[str], Optional[int]]:
    path = osp.join(dirname, basename)
    with open(path, 'r', encoding='utf-8-sig') as file:
        lines = file.read().splitlines()

    error1 = lines.count('END') > 1
    if error1:
        # https://forum.gravon.de/phpBB/viewtopic.php?p=24838&highlight=#24838
        # classic.2003.06.07.505.gsn
        ends = [
            idx
            for idx, line in enumerate(lines)
            if line == 'END'
        ]
        assert ends[-1] == len(lines) - 2
        lines = lines[:ends[-1]]

    error2 = lines[-2] != 'END'
    if error2:
        # https://forum.gravon.de/phpBB/viewtopic.php?p=24837&highlight=#24837
        # classic.2003.09.26.5746.gsn
        idx = lines.index('END')
        lines = lines[:idx] + lines[(idx + 2):] + lines[idx:(idx + 2)]

    error3 = False

    if not (error1 or error2 or error3):
        return None, None

    with open(path, 'w') as file:
        file.writelines([
            line + '\n'
            for line in lines
        ])

    error_code = error3 * 4 + error2 * 2 + error1 * 1
    return basename, error_code

def _xml(dirname: str, basename: str) -> Tuple[Optional[str], Optional[int]]:
    path = osp.join(dirname, basename)
    tree = lxml.etree.parse(path)

    error1 = False
    error2 = False

    # https://forum.gravon.de/phpBB/viewtopic.php?p=24839&highlight=#24839
    # ultimate lightning-2005.5-2105.xml and 35 other files
    moves_J_file = tree.xpath('.//move[starts-with(@source, "J") or starts-with(@target, "J")]')
    error3 = len(moves_J_file) > 0
    if error3:
        for move in moves_J_file:
            for square in ('source', 'target'):
                move.attrib[square] = move.attrib[square].replace('J', 'K')

    if not (error1 or error2 or error3):
        return None, None

    with open(path, 'w') as file:
        file.write(lxml.etree
            .tostring(
                tree,
                xml_declaration=True,
                encoding='UTF-8',
                pretty_print=True
            )
            .decode('utf-8')
        )

    error_code = error3 * 4 + error2 * 2 + error1 * 1
    return basename, error_code

def _subset(dirname: str, txt_files: pd.DataFrame, repairer: Callable[[str, str], Tuple[str, int]]) -> List[Tuple[str, int]]:
    return [
        repairer(dirname, row.filename)
        for row in tqdm(txt_files.itertuples(), total=txt_files.shape[0])
    ]

def directory(dirname: str, txt_files: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        data=[
            (basename, error_code)
            for ext, repairer in [
                ('.gsn', _gsn),
                ('.xml', _xml)
            ]
            for basename, error_code in _subset(dirname, txt_files.query('filename.str.endswith(@ext)'), repairer)
            if basename and error_code  # filter out files that were already clean
        ],
        columns=[
            'filename', 'error_code'
        ]
    )


#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd
import plotnine as p9

from gravon.setup import row_labels, col_labels

def heatmap(data: np.array, format_string=None):
    N = data.sum()
    mu = data.mean()
    ds = (pd
        .DataFrame(data, index=row_labels, columns=col_labels)
        .rename_axis('row')
        .reset_index()
        .melt(id_vars='row', var_name='col')
        .assign(
            rel = lambda r: r.value / mu,
            log = lambda r: np.log10(r.rel)
        )
    )
    rs = (ds
        .groupby('row')
        .agg(value = ('value', 'sum'))
        .reset_index()
        .assign(
            col = 'rows',
            value = lambda r: r.value / N,
            rel = lambda r: r.value * 4,
            log = lambda r: np.log10(r.rel)
        )
    )
    cs = (ds
        .groupby('col')
        .agg(value = ('value', 'sum'))
        .reset_index()
        .assign(
            row = 'cols',
            value = lambda r: r.value / N,
            rel = lambda r: r.value * 10,
            log = lambda r: np.log10(r.rel)
        )
    )
    df = (pd
        .concat([ds, rs, cs])
        .astype(dtype={
            'row': pd.CategoricalDtype(categories=['1', '2', '3', '4', '', 'cols']),
            'col': pd.CategoricalDtype(categories=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', '', 'rows'])
        })
    )

    return (p9.ggplot(df, p9.aes(y='row', x='col'))
        # https://stackoverflow.com/a/62161556/819272
        # Plotnine does not support changing the position of any axis.
        + p9.coord_equal()
        + p9.geom_tile(p9.aes(fill='log'))
        + p9.geom_text(p9.aes(label='value'), format_string=format_string, size=8)
        + p9.scale_y_discrete(drop=False)
        + p9.scale_x_discrete(drop=False)
        + p9.scale_fill_gradientn(colors=['#63BE7B', '#FFEB84', '#F8696B'], guide=False)
        + p9.theme(axis_ticks=p9.element_blank(), axis_title=p9.element_blank(), panel_grid=p9.element_blank())
    )

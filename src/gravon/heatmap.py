
#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd
import plotnine as p9

from gravon.setup import row_labels, col_labels

def heatmap(array: np.array, title_string=None, format_string=None, normalize=True, rotated=False, margins=(0, 1), margin_fill=True, axis_text=True):
    mu = array.mean()
    data = (pd
        .DataFrame(array, index=row_labels, columns=col_labels)
        .rename_axis('row')
        .reset_index()
        .melt(id_vars='row', var_name='col')
        .assign(
            scale = lambda r: np.log10(r.value / mu)
        )
    )
    rows = (data
        .groupby('row')
        .agg(value = ('value', 'sum'))
        .reset_index()
        .assign(
            col = 'rows',
            scale = lambda r: np.log10(r.value / (10 * mu)) if margin_fill else np.nan,
            value = lambda r: r.value / (40 * mu) if normalize else r.value
        )
    ) if 0 in margins else pd.DataFrame()
    cols = (data
        .groupby('col')
        .agg(value = ('value', 'sum'))
        .reset_index()
        .assign(
            row = 'cols',
            scale = lambda r: np.log10(r.value / (4 * mu)) if margin_fill else np.nan,
            value = lambda r: r.value / (40 * mu) if normalize else r.value
        )
    ) if 1 in margins else pd.DataFrame()
    grand = (pd.DataFrame(
        data=[('cols', 'rows', rows.value.sum(), np.nan)],
        columns=['row', 'col', 'value', 'scale']
    )) if 0 in margins else pd.DataFrame()

    row_cat = row_labels.copy()
    row_cat += [''] if (0 in margins and margin_fill) else []
    row_cat += ['cols']
    row_cat = list(reversed(row_cat)) if rotated else row_cat

    col_cat = col_labels.copy()
    col_cat = list(reversed(col_cat)) if rotated else col_cat
    col_cat += [''] if (1 in margins and margin_fill) else []
    col_cat += ['rows']

    df = (pd
        .concat([data, rows, cols, grand])
        .astype(dtype={
            'row': pd.CategoricalDtype(categories=row_cat),
            'col': pd.CategoricalDtype(categories=col_cat)
        })
    )

    axis_text = p9.element_blank() if not axis_text else None

    # https://stackoverflow.com/a/62161556/819272
    # Plotnine does not support changing the position of any axis.
    return (
          p9.ggplot(df, p9.aes(y='row', x='col'))
        + p9.ggtitle(title_string)
        + p9.coord_equal()
        + p9.geom_tile(p9.aes(fill='scale'))
        + p9.geom_text(p9.aes(label='value'), format_string=format_string, size=7)
        + p9.scale_y_discrete(drop=False)
        + p9.scale_x_discrete(drop=False)
        + p9.scale_fill_gradientn(colors=['#63BE7B', '#FFEB84', '#F8696B'], na_value='#CCCCCC', guide=False)
        + p9.theme(axis_text=axis_text, axis_ticks=p9.element_blank(), axis_title=p9.element_blank(), panel_grid=p9.element_blank())
    )

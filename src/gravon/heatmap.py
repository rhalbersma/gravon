
#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd
import plotnine as p9

from gravon.setup import row_labels, col_labels

def tidy1(array: np.array, margins=(0, 1), margin_fill=True, normalize=True, rotated=False) -> pd.DataFrame:
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

    return (pd
        .concat([data, rows, cols, grand])
        .astype(dtype={
            'row': pd.CategoricalDtype(categories=row_cat),
            'col': pd.CategoricalDtype(categories=col_cat)
        })
    )

def tidy2(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return (pd
        .merge(
            df1.drop(columns='scale'), 
            df2.drop(columns='scale'),
            on = ['row', 'col']
        )
        .assign(
            value = lambda r: r.value_y / r.value_x,
            scale = lambda r: np.log10(r.value)
        )
        .drop(columns=['value_x', 'value_y'])
    )

def setup_heatmap0(df: pd.DataFrame, format_string=None, axis_text=True):
    # https://stackoverflow.com/a/62161556/819272
    # Plotnine does not support changing the position of any axis.
    return (
          p9.ggplot(df, p9.aes(y='row', x='col'))
        + p9.coord_equal()
        + p9.geom_tile(p9.aes(fill='scale'))
        + p9.geom_text(p9.aes(label='value'), format_string=format_string, size=7)
        + p9.scale_y_discrete(drop=False)
        + p9.scale_x_discrete(drop=False)
        + p9.scale_fill_gradientn(colors=['#63BE7B', '#FFEB84', '#F8696B'], na_value='#CCCCCC', guide=False)
        + p9.theme(
            axis_text =p9.element_blank() if not axis_text else None, 
            axis_ticks=p9.element_blank(), 
            axis_title=p9.element_blank(), 
            panel_grid=p9.element_blank()
        )
    )

def setup_heatmap1(array: np.array, format_string=None, axis_text=True, margins=(0, 1), margin_fill=True, normalize=True, rotated=False):
    df = tidy1(array, margins=margins, margin_fill=margin_fill, normalize=normalize, rotated=rotated)
    return setup_heatmap0(df, format_string=format_string, axis_text=axis_text) 

def setup_heatmap2(array1: np.array, array2: np.array, format_string=None, axis_text=True, margins=(0, 1), margin_fill=True, normalize=True, rotated=False):
    df1 = tidy1(array1, margins=margins, margin_fill=margin_fill, normalize=normalize, rotated=rotated)
    df2 = tidy1(array2, margins=margins, margin_fill=margin_fill, normalize=normalize, rotated=rotated)
    df = tidy2(df1, df2)
    return setup_heatmap0(df, format_string=format_string, axis_text=axis_text)
 
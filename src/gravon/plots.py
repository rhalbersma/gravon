
#          Copyright Rein Halbersma 2018-2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd
import plotnine as p9

from gravon.setup import row_labels, col_labels

def tidy1(array: np.array, log10_scale, margins, margin_fill, normalize, rotate) -> pd.DataFrame:
    id_scale = lambda x: x
    fn_scale = np.log10 if log10_scale else id_scale
    N = array.sum()
    data = (pd
        .DataFrame(array, index=row_labels, columns=col_labels)
        .rename_axis('row')
        .reset_index()
        .melt(id_vars='row', var_name='col')
        .assign(
            scale = lambda r: fn_scale(r.value / (N / 40))
        )
    )
    rows = (data
        .groupby('row')
        .agg(value = ('value', 'sum'))
        .reset_index()
        .assign(
            col = 'Total',
            scale = lambda r: fn_scale(r.value / (N / 4)) if margin_fill else np.nan,
            value = lambda r: r.value / N if normalize else r.value
        )
    ) if 0 in margins else pd.DataFrame()
    cols = (data
        .groupby('col')
        .agg(value = ('value', 'sum'))
        .reset_index()
        .assign(
            row = 'Total',
            scale = lambda r: fn_scale(r.value / (N / 10)) if margin_fill else np.nan,
            value = lambda r: r.value / N if normalize else r.value
        )
    ) if 1 in margins else pd.DataFrame()
    grand = (data
        .agg(value = ('value', 'sum'))
        .reset_index()
        .assign(
            row = 'Total',
            col = 'Total',
            scale = np.nan,
            value = lambda r: r.value / N if normalize else r.value
        )
    ) if len(margins) > 0 else pd.DataFrame()

    row_cat = row_labels.copy()
    row_cat += [''] if ((0 in margins) and margin_fill) else []
    row_cat += ['Total'] if len(margins) > 0 else []
    row_cat = list(reversed(row_cat)) if rotate else row_cat

    col_cat = col_labels.copy()
    col_cat = list(reversed(col_cat)) if rotate else col_cat
    col_cat += [''] if ((1 in margins) and margin_fill) else []
    col_cat += ['Total'] if len(margins) > 0 else []

    return (pd
        .concat([data, rows, cols, grand])
        .astype(dtype={
            'row': pd.CategoricalDtype(categories=row_cat),
            'col': pd.CategoricalDtype(categories=col_cat)
        })
    )

def tidy2(df_numer: pd.DataFrame, df_denom: pd.DataFrame, log10_scale) -> pd.DataFrame:
    id_scale = lambda x: x
    fn_scale = np.log10 if log10_scale else id_scale
    return (pd
        .merge(
            df_numer.drop(columns='scale'), 
            df_denom.drop(columns='scale'),
            on=['row', 'col'], 
            suffixes=['_numer', '_denom']
        )
        .assign(
            value = lambda r: r.value_numer / r.value_denom,
            scale = lambda r: fn_scale(r.value)
        )
        .drop(columns=['value_numer', 'value_denom'])
    )

def setup_heatmap0(df: pd.DataFrame, format_string, axis_text):
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

def setup_heatmap1(array: np.array, format_string=None, axis_text=True, log10_scale=True, margins=(0, 1), margin_fill=True, normalize=False, rotate=False):
    df = tidy1(array, log10_scale, margins, margin_fill, normalize, rotate)
    return setup_heatmap0(df, format_string, axis_text) 

def setup_heatmap2(numer: np.array, denom: np.array, format_string=None, axis_text=True, log10_scale=True, margins=(0, 1), margin_fill=True, normalize=False, rotate=False):
    df_numer = tidy1(numer, log10_scale, margins, margin_fill, normalize, rotate)
    df_denom = tidy1(denom, log10_scale, margins, margin_fill, normalize, rotate)
    df = tidy2(df_numer, df_denom, log10_scale)
    return setup_heatmap0(df, format_string, axis_text)
 
"""
Functions to create custom palettes.
"""

import pandas as pd
import seaborn as sns
import colorsys
import matplotlib.colors
from typing import Dict, Iterable, Any
import numpy as np


##


# Custom palette
ten_godisnot = [

    '#001E09', 
    '#885578',
    '#FF913F', 
    '#1CE6FF', 
    '#549E79', 
    '#C9E850',
    '#EEC3FF', 
    '#FFEF00',
    '#D157A0', 
    '#922329'
    
]
ten_godisnot = [ matplotlib.colors.hex2color(x) for x in ten_godisnot ]


##


def _change_color(color, saturation=0.5, lightness=0.5):
    
    r, g, b = color
    h, s, l = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(h, lightness, saturation)
    
    return (r, g, b)


##


def create_palette(
    df: pd.DataFrame, 
    var: str, 
    palette: str = None, 
    saturation: float = None, 
    col_list: Iterable[str|Any] = None, 
    lightness: float = None,
    add_na: bool = False
    ) -> Dict[str,str] :
    """
    Create a color palette from a pd.DataFrame, a column, a palette or a list of colors.

    Parameters
    ----------
        df: pd.DataFrame
            DataFrame storing "var" categories
        var: str
            Column in df to search for categories 
        palette: str, optional
            Color palette from seaborn. Default is None
        col_list: Iterable[str|Any], optional
            Color list. Must be values recognized by matplotlib. Default is None
        saturation: float, optional
            Saturation value. Default is None 
        lightness: float, optional
            Lightness value. Default is None
        add_na: bool, optional
            Add value for np.nan or "unassigned" category. Default is False
    
    Returns
    -------
        colors: dict
            mapping of category : color
    """


    cats = df[var].unique()
    n = len(cats)
    
    if col_list is not None:
        cols = col_list[:n]
    elif palette is not None:
        cols = sns.color_palette(palette, n_colors=n)
    else:
        raise ValueError('Provide one between palette and col_list!')
    
    colors = { k: v for k, v in zip(cats, cols)}
    
    if saturation is not None:
        colors = { 
            k: _change_color(colors[k], saturation=saturation) \
            for k in colors 
        }
    if lightness is not None:
        colors = { 
            k: _change_color(colors[k], lightness=lightness) \
            for k in colors 
        }
    
    if add_na:
        colors.update({'unassigned':'lightgrey', np.nan:'lightgrey'})
     
    return colors


##
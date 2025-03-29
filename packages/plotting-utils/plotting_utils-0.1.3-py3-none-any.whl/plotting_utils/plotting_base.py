"""
Plotting utilities and 'base plots', i.e., simple plots returning an Axes object.
"""

import numpy as np 
import pandas as pd 
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import textalloc as ta
from matplotlib.lines import Line2D 
from statannotations.Annotator import Annotator 
from sklearn.metrics.pairwise import pairwise_distances
from scipy.cluster.hierarchy import linkage, leaves_list
from typing import Dict, Iterable, Any, Tuple
from .colors import *
from .utils import *
plt.style.use('default')


##


# Params
axins_pos = {

    'v2' : ( (.95,.75,.01,.22), 'left', 'vertical' ),
    'v3' : ( (.95,.05,.01,.22), 'left','vertical' ),
    'v1' : ( (.05,.75,.01,.22), 'right', 'vertical' ),
    'v4' : ( (.05,.05,.01,.22), 'right', 'vertical' ),

    'h2' : ( (1-.27,.95,.22,.01), 'bottom', 'horizontal' ),
    'h3' : ( (1-.27,.05,.22,.01), 'top', 'horizontal' ),
    'h1' : ( (0.05,.95,.22,.01), 'bottom', 'horizontal' ),
    'h4' : ( (0.05,.05,.22,.01), 'top', 'horizontal' ),

    'outside' : ( (1.05,.25,.03,.5), 'right', 'vertical' )
}


##


def set_rcParams():
    """
    Applies Nature Methods journal-style settings for matplotlib figures.
    """
    plt.rcParams.update({

        # Figure dimensions and DPI
        'figure.figsize': (3.5,3.5),  # Recommended size for 1-row, 2-column figure
        'figure.dpi': 200,           # High DPI for print quality

        # Font settings
        'font.size': 10,                # Base font size
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial'],  # Preferred font for Nature figures

        # Axes properties
        'axes.titlesize': 10,           # Title font size
        'axes.labelsize': 10,           # Label font size
        'axes.linewidth': 0.5,         # Minimum line width for axes

        # Tick properties
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.major.size': 3,         # Major tick length
        'ytick.major.size': 3,
        'xtick.minor.size': 1.5,       # Minor tick length
        'ytick.minor.size': 1.5,
        'xtick.major.width': 0.5,      # Tick width
        'ytick.major.width': 0.5,

        # Legend properties
        'legend.fontsize': 10, 

        # # Line properties
        'lines.linewidth': 1,          # Line width for main data elements
        'lines.markersize': 4,         # Marker size
    })


##


def create_handles(mapping, marker='o', size=10, width=0.5):
    """
    Create quick and dirty circular and labels for legends.
    """

    handles = [ 
        (Line2D([], [], 
        marker=marker, 
        label=l, 
        linewidth=0,
        markersize=size, 
        markeredgewidth=width, 
        markeredgecolor='k', 
        markerfacecolor=c)) \
        for l, c in mapping.items()
    ]

    return handles


##


def add_cbar(
    x: Iterable[int|float], 
    palette: str = 'viridis', 
    ax: matplotlib.axes.Axes = None, 
    label_size: float = None, 
    ticks_size: float = 8, 
    vmin: int|float = None, 
    vmax: int|float = None, 
    label: str = None, 
    layout: str|Dict[str,Tuple[Tuple[float,float,float,float],str,str]] = 'outside'
    ):
    """
    Draw a colorbar on the provided ax=matplotlib.axes.Axes object inset.

    Parameters
    ----------
    x: Iterable
        Array of numeric values from which the colorbar should take values. 
    palette: str, optional
        Seaborn palette. Default: viridis.
    ax: matplotlib.axes.Axes, optional.
        Ax object to draw on. Default: None
    label_size: float, optional
        Label size for colobar. Default: None (i.e., set with rcParams)
    ticks_size: float, optional
        Ticks size for colobar. Default: None (i.e., set with rcParams)
    vmin: float, optional
        Min value to clip the colorbar. Default: None (i.e., 25th percentile of x)
    vmax: float, optional
        Max value to clip the colorbar. Default: None (i.e., 75th percentile of x)
    label: str, optional
        Colorbar label. Default: None
    layout: str or tuple, optional
        Layout of the colorbar. Default: "outside"

    Notes
    -----
    Example layout: 'h1', or equivalently ( (0.05,.95,.22,.01), 'bottom', 'horizontal' )
    """

    if layout in axins_pos:
        pos, xticks_position, orientation = axins_pos[layout]
    else:
        pos, xticks_position, orientation = layout
        
    cmap = matplotlib.colormaps[palette]
    if vmin is None and vmax is None:
        norm = matplotlib.colors.Normalize(
            vmin=np.percentile(x, q=25), vmax=np.percentile(x, q=75))
    else:
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    axins = ax.inset_axes(pos) 
    
    cb = plt.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), 
        cax=axins, orientation=orientation, ticklocation=xticks_position
    )
    cb.set_label(label=label, size=label_size, loc='center')

    if orientation == 'vertical':
        cb.ax.tick_params(axis="y", labelsize=ticks_size)
    else:
        cb.ax.tick_params(axis="x", labelsize=ticks_size)
    

##


def add_legend(
    colors: Dict[str,Any],
    label: str = None, 
    ax: matplotlib.axes.Axes = None, 
    loc: str = 'upper left', 
    bbox_to_anchor: Tuple[float,float] = (1, 1), 
    artists_size: float = 10, 
    label_size: float = None, 
    ticks_size: float = None, 
    ncols: int = 1, 
    only_top: str|int = 'all'
    ):
    """
    Draw a legend on a ax: matplotlib.axes.Axes object.

    Parameters
    ----------

    colors: Dict[str|Any],
        mapping of keys to colors.
    label: str, optional
        Legend label. Default is None
    ax: matplotlib.axes.Axes, optional
        ax to draw on. Default is False
    loc: str, optional
        loc kwarg from ax.legend(). Which part of the legend to anchor. Default is 'upper left'
    bbox_to_anchor: tuple, optional
        bbox_to_anchor kwarg from ax.legend(). Which ax box to anchor. Default is (1,1)
    artists_size: float, optional
        Size of artists. Default is 10
    label_size: float, optional
        Legend title size. Default is None
    ticks_size: float, optional
        Legend ticks size. Default is None
    ncols: int, optional
        N of colors to arrange artists on. Default is 1
    only_top: str ot int, optional
        N of categories to display. Default is "all"

    """

    # Remove np.nan mappings from colors, if present
    try:
        del colors['unassigned']
        del colors[np.nan]
    except:
        pass

    if only_top != 'all':
        colors = { k : colors[k] for i, k in enumerate(colors) if i < int(only_top) }

    handles = create_handles(colors, size=artists_size)
    legend = ax.legend(
        handles, 
        colors.keys(), 
        frameon=False, 
        loc=loc, 
        fontsize=ticks_size, 
        title_fontsize=label_size, 
        ncol=ncols, 
        title=label if label is not None else None, 
        bbox_to_anchor=bbox_to_anchor
    )
    ax.add_artist(legend)


##


def format_ax(
    ax: matplotlib.axes.Axes = None, 
    title: str = None, 
    xlabel: str = None, 
    ylabel: str = None, 
    xticks: Iterable[Any] = None, 
    yticks: Iterable[Any] = None, 
    rotx: float = 0, 
    roty: float = 0, 
    axis: bool = True,
    xlabel_size: float = None, 
    ylabel_size: float = None,
    xticks_size: float = None, 
    yticks_size: float = None,
    title_size: float = None, 
    log: bool = False, 
    reduced_spines: bool = False
    ) -> matplotlib.axes.Axes:
    """
    Format labels, ticks and stuff of an ax: matplotlib.axes.Axes object.
    """

    if log:
        ax.set_yscale('log')
    
    if title is not None:
        ax.set(title=title)
    
    if xlabel is not None:
        ax.set(xlabel=xlabel)
    
    if xlabel is not None:
        ax.set(ylabel=ylabel)

    if xticks is not None:
        ax.set_xticks([ i for i in range(len(xticks)) ])
        ax.set_xticklabels(xticks)
    if yticks is not None:
        ax.set_yticks([ i for i in range(len(yticks)) ])
        ax.set_yticklabels(yticks)

    if xticks_size is not None:
        ax.xaxis.set_tick_params(labelsize=xticks_size)
    if yticks_size is not None:
        ax.yaxis.set_tick_params(labelsize=yticks_size)

    if xlabel_size is not None:
        ax.xaxis.label.set_size(xlabel_size)
    if ylabel_size is not None:
        ax.yaxis.label.set_size(ylabel_size)

    ax.tick_params(axis='x', labelrotation = rotx)
    ax.tick_params(axis='y', labelrotation = roty)

    if title_size is not None:
        ax.set_title(title, fontdict={'fontsize': title_size})
    
    if reduced_spines:
        ax.spines[['right', 'top']].set_visible(False)
    
    if not axis:
        ax.axis('off')

    return ax


##


def add_wilcox(
    df: pd.DataFrame, 
    x: str, 
    y: str, 
    pairs: Iterable[Iterable[str]], 
    ax:  matplotlib.axes.Axes = None, 
    order: Iterable[str] = None
    ):
    """
    Add statistical annotations (basic tests from statannotations).
    """
    annotator = Annotator(ax, pairs, data=df, x=x, y=y, order=order)
    annotator.configure(
        test='Mann-Whitney', text_format='star', show_test_name=False,
        line_height=0.001, text_offset=3
    )
    annotator.apply_and_annotate()


##


def remove_ticks(ax):
    """
    Remove ticks form ax x- and y-axis.
    """
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.tick_params(axis='both', which='both', length=0)


##


def add_labels_on_loc(df, x, y, by, ax=None, s=10):
    """
    Add categorical labels on loc on a scatterplot.
    """
    coords = df.loc[:, [x, y, by]].groupby(by).median()
    for label in coords.index:
        x, y = coords.loc[label, :].tolist()
        ax.text(x, y, label, fontsize=s)


##



def scatter(
    df: pd.DataFrame, 
    x: str, 
    y:str, 
    by: str = None, 
    color: str = 'k',
    categorical_cmap: str|Dict[str,Any] = 'tab10', 
    continuous_cmap: str = 'viridis', 
    marker: str = 'o', 
    size: float|str = 1.0, 
    alpha: float = 1.0, 
    ax: matplotlib.axes.Axes = None, 
    scale_x: float = None, 
    vmin: float = None, 
    vmax: float = None
    ) -> matplotlib.axes.Axes:
    """
    Base scatter plot.
    """

    # Take x- y- arrays
    x = df[x]; y = df[y]

    # Handle size
    s = 1
    if isinstance(size, float) or isinstance(size, int):
        s = size
    elif isinstance(size, str) and size in df.columns:
        s = df[size].values
        if scale_x is not None:
            s = s * scale_x
    else:
        raise ValueError(f'Size {size} can be either a numeric value or a column of provided df')

    # Handle colors and by
    if by is None:
        ax.scatter(x, y, c=color, marker=marker, s=s, alpha=alpha)

    elif by is not None and by in df.columns:
        
        # Categorical
        if pd.api.types.is_string_dtype(df[by]) or df[by].dtype == 'category':
            
            if isinstance(categorical_cmap, str):
                _cmap = create_palette(df, by, palette=categorical_cmap)
            else:
                _cmap = categorical_cmap

            assert all([ x in _cmap for x in df[by].unique() ])
            colors = [ _cmap[x] for x in df[by] ]
            ax.scatter(
                x, y, 
                c=colors,
                marker=marker, s=s, alpha=alpha 
            )

        # Numeric
        elif pd.api.types.is_numeric_dtype(df[by]):

            vmin = vmin if vmin is not None else np.percentile(df[by],25)
            vmax = vmax if vmax is not None else np.percentile(df[by],75)
            ax.scatter(
                x, y, 
                c=df[by], cmap=continuous_cmap, vmin=vmin, vmax=vmax, 
                marker=marker, s=s, alpha=alpha 
            )

        else:
            raise ValueError(f'Unknown dtype: {by}')
    
    else:
        raise KeyError(f'{by} not in df.columns!')

    return ax


##


def dist(
    df: pd.DataFrame, 
    x: str, 
    by: str = None, 
    color: str = 'k',
    categorical_cmap: str|Dict[str,Any] = 'tab10', 
    alpha: float = .4, 
    ax: matplotlib.axes.Axes = None, 
    fill: bool = True,
    linewidth: float = .5
    ) -> matplotlib.axes.Axes:
    """
    Basic distribution plot.
    """

    # Handle colors and by
    if by is None:
        sns.kdeplot(
            df[x], color=color, ax=ax, fill=fill, 
            alpha=alpha, linewidth=linewidth
        )
        
    elif by is not None and by in df.columns:
        
        # Categorical
        if pd.api.types.is_string_dtype(df[by]) or df[by].dtype == 'category':
            
            if isinstance(categorical_cmap, str):
                _cmap = create_palette(df, by, palette=categorical_cmap)
            else:
                _cmap = categorical_cmap

            assert all([ x in _cmap for x in df[by].unique() ])

            for cat in df[by].unique():
                sns.kdeplot(
                    df.loc[df[by]==cat, x], 
                    color=_cmap[cat], ax=ax, fill=fill, 
                    alpha=alpha, linewidth=linewidth
                )

        else:
            raise ValueError(f'{by} must be categorical or string!')
    
    else:
        raise KeyError(f'{by} not in df.columns!')

    return ax


##


def counts_plot(
    df: pd.DataFrame, 
    x: str, 
    width: float = .8, 
    alpha: float = .5, 
    color: str = '#105D62', 
    edgecolor: str = 'k', 
    linewidth: float = .5, 
    with_label: bool = True,
    label_size: float = None,
    ax: matplotlib.axes.Axes = None
    ) -> matplotlib.axes.Axes:
    """
    Basic counts plot.
    """

    counts = df[x].value_counts()
    ax.bar(
        np.arange(counts.size), counts, 
        align='center', 
        width=width, 
        alpha=alpha, 
        color=color, 
        edgecolor=edgecolor, 
        linewidth=linewidth
    )
    if with_label:
        ax.bar_label(ax.containers[0], padding=0, fontsize=label_size)
    
    ax.set(xlabel='Value', ylabel='n')

    return ax


##


def bar(
    df: pd.DataFrame, 
    x: str, 
    y: str, 
    by: str = None, 
    color: str = None,
    edgecolor: str = 'k',
    categorical_cmap: str|Dict[str,Any] = 'tab10', 
    x_order: Iterable[str] = None,
    by_order: Iterable[str] = None,
    width: float|str = .8, 
    linewidth: float = .5,
    alpha: float = .8, 
    ax: matplotlib.axes.Axes = None, 
    ) -> matplotlib.axes.Axes:
    """
    Basic bar plot.
    """

    # Handle colors and by
    if by is None:
        sns.barplot(
            data=df, x=x, y=y, ax=ax, 
            order=x_order, 
            color=color,
            width=width, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth
        )
        
    elif by is not None and by in df.columns:
        
        # Categorical
        if pd.api.types.is_string_dtype(df[by]) or df[by].dtype == 'category':
            
            if isinstance(categorical_cmap, str):
                _cmap = create_palette(df, by, palette=categorical_cmap)
            else:
                _cmap = categorical_cmap

            assert all([ x in _cmap for x in df[by].unique() ])
            sns.barplot(
                data=df, x=x, y=y, ax=ax, 
                order=x_order, 
                hue=by, hue_order=by_order, palette=_cmap,
                width=width, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth
            )
            ax.get_legend().remove()

        else:
            raise ValueError(f'{by} must be categorical or string!')
    
    else:
        raise KeyError(f'{by} not in df.columns!')

    return ax


##


def box(
    df: pd.DataFrame, 
    x: str, 
    y: str, 
    by: str = None, 
    color: str = None,
    categorical_cmap: str|Dict[str,Any] = 'tab10', 
    x_order: Iterable[str] = None,
    add_stats: bool = False,
    pairs: Iterable[Iterable[str]] = None, 
    by_order: Iterable[str] = None,
    width: float|str = .8, 
    ax: matplotlib.axes.Axes = None, 
    kwargs: Dict[str,Any] = {}
    ) -> matplotlib.axes.Axes:
    """
    Base box plot.
    """

    # Handle params
    params = {   
        'showcaps' : False,
        'fliersize': 0,
        'boxprops' : {'edgecolor': 'black', 'linewidth': .8}, 
        'medianprops': {"color": "black", "linewidth": 1.5},
        'whiskerprops':{"color": "black", "linewidth": 1.2}
    }
    params = update_params(params, kwargs)
    
    # Handle colors and by
    if by is None:
        sns.boxplot(
            data=df, x=x, y=y, ax=ax, 
            order=x_order, 
            color=color,
            width=width, 
            **params
        )
        
    elif by is not None and by in df.columns:
        
        # Categorical
        if pd.api.types.is_string_dtype(df[by]) or df[by].dtype == 'category':
            
            if isinstance(categorical_cmap, str):
                _cmap = create_palette(df, by, palette=categorical_cmap)
            else:
                _cmap = categorical_cmap

            assert all([ x in _cmap for x in df[by].unique() ])
            sns.boxplot(
                data=df, x=x, y=y, ax=ax, 
                order=x_order, 
                hue=by, hue_order=by_order, palette=_cmap,
                width=width, 
                **params
            )
            ax.get_legend().remove()

        else:
            raise ValueError(f'{by} must be categorical or string!')
    
    else:
        raise KeyError(f'{by} not in df.columns!')

    if add_stats:
        add_wilcox(df, x, y, pairs, ax, order=x_order)

    return ax


##


def strip(
    df: pd.DataFrame, 
    x: str, 
    y: str, 
    by: str = None, 
    color: str = None,
    edgecolor: str = 'k',
    linewidth: float = .1,
    categorical_cmap: str|Dict[str,Any] = 'tab10', 
    x_order: Iterable[str] = None,
    add_stats: bool = False,
    pairs: Iterable[Iterable[str]] = None, 
    by_order: Iterable[str] = None,
    size: float|str = 5, 
    ax: matplotlib.axes.Axes = None, 
    ) -> matplotlib.axes.Axes:
    """
    Base stripplot.
    """
    
    np.random.seed(123)
    
    # Handle colors and by
    if by is None:
        sns.stripplot(
            data=df, x=x, y=y, ax=ax, 
            order=x_order, 
            color=color,
            edgecolor=edgecolor,
            linewidth=linewidth,
            size=size
        )
        
    elif by is not None and by in df.columns:
        
        # Categorical
        if pd.api.types.is_string_dtype(df[by]) or df[by].dtype == 'category':
            
            if isinstance(categorical_cmap, str):
                _cmap = create_palette(df, by, palette=categorical_cmap)
            else:
                _cmap = categorical_cmap

            assert all([ x in _cmap for x in df[by].unique() ])
            sns.stripplot(
                data=df, x=x, y=y, ax=ax, 
                order=x_order, 
                dodge=True,
                hue=by, hue_order=by_order, palette=_cmap,
                edgecolor=edgecolor,
                linewidth=linewidth,
                size=size
            )
            ax.get_legend().remove()

        else:
            raise ValueError(f'{by} must be categorical or string!')
    
    else:
        raise KeyError(f'{by} not in df.columns!')

    if add_stats:
        add_wilcox(df, x, y, pairs, ax, order=x_order)

    return ax


##


def violin(
    df: pd.DataFrame, 
    x: str, 
    y: str, 
    by: str = None, 
    color: str = None,
    categorical_cmap: str|Dict[str,Any] = 'tab10', 
    x_order: Iterable[str] = None,
    add_stats: bool = False,
    pairs: Iterable[Iterable[str]] = None, 
    by_order: Iterable[str] = None,
    linewidth: float|str = .5, 
    ax: matplotlib.axes.Axes = None, 
    kwargs: Dict[str,Any] = {}
    ) -> matplotlib.axes.Axes:
    """
    Base violinplot.
    """

    params = {   
        'inner' : 'quart'
    }    
    params = update_params(params, kwargs)

    # Handle colors and by
    if by is None:
        sns.violinplot(
            data=df, x=x, y=y, ax=ax, 
            order=x_order, 
            color=color,
            linewidth=width, 
            **params
        )
        
    elif by is not None and by in df.columns:
        
        # Categorical
        if pd.api.types.is_string_dtype(df[by]) or df[by].dtype == 'category':
            
            if isinstance(categorical_cmap, str):
                _cmap = create_palette(df, by, palette=categorical_cmap)
            else:
                _cmap = categorical_cmap

            assert all([ x in _cmap for x in df[by].unique() ])
            sns.violinplot(
                data=df, x=x, y=y, ax=ax, 
                order=x_order, 
                dodge=True,
                hue=by, hue_order=by_order, palette=_cmap,
                linewidth=linewidth, 
                **params
            )
            ax.get_legend().remove()

        else:
            raise ValueError(f'{by} must be categorical or string!')
    
    else:
        raise KeyError(f'{by} not in df.columns!')

    if add_stats:
        add_wilcox(df, x, y, pairs, ax, order=x_order)

    return ax


##


def _reorder(X, metric='euclidean', method='average', n_jobs=-1):
    """
    Reorder rows of an array X.
    """
    D = pairwise_distances(X, metric=metric, n_jobs=n_jobs)
    order = leaves_list(linkage(D, method=method))

    return order


##


def plot_heatmap(
    df: pd.DataFrame, 
    palette: str = 'mako', 
    ax: matplotlib.axes.Axes = None, 
    title: str = None, 
    x_names: bool = True, y_names: bool = True, 
    x_names_size: float = 7, y_names_size: float = 7, 
    xlabel: Iterable[Any] = None, ylabel: Iterable[Any] = None, 
    annot: bool = False, annot_size: float = 5, 
    label: str = None, shrink: float = 1.0, cb: bool = True, 
    vmin: float = None, vmax: float = None, 
    cluster_rows: bool = False, 
    cluster_cols: bool = False, 
    fmt: str = "%d",
    outside_linewidth: float = 1, linewidths: float = 0, 
    linecolor: Any = 'white'
    ) -> matplotlib.axes.Axes:
    """
    Simple heatmap.
    """
    
    # Re-order rows and cols
    row_order = _reorder(df.values) if cluster_rows else range(df.shape[0])
    col_order =  _reorder(df.values.T) if cluster_cols else range(df.shape[1])   
    df_plot = df.iloc[row_order, col_order].copy()

    # Main plot
    ax = sns.heatmap(
        data=df_plot, 
        ax=ax, 
        robust=True, 
        cmap=palette, 
        annot=annot, 
        xticklabels=x_names, 
        yticklabels=y_names, 
        fmt=fmt, 
        annot_kws={'size':annot_size}, 
        cbar=cb,
        cbar_kws={'fraction':0.05, 'aspect':35, 'pad': 0.02, 'shrink':shrink, 'label':label},
        vmin=vmin, 
        vmax=vmax, 
        linewidths=linewidths, 
        linecolor=linecolor
    )
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=x_names_size)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=y_names_size)

    # Prettify spines
    for _, spine in ax.spines.items():
        spine.set_visible(True)
        spine.set_linewidth(outside_linewidth)

    return ax


##


def stem_plot(df, x, ax=None):
    """
    Create a stem plot.
    """
    ax.hlines(y=df.index, xmin=0, xmax=df[x], color='darkgrey')
    ax.plot(df[x][df[x]>=0], df[x].index[df[x]>=0], "o", color='r')
    ax.plot(df[x][df[x]<0], df[x].index[df[x]<0], "o", color='b')
    ax.axvline(color="black", linestyle="--")
    ax.invert_yaxis()
    return ax


##


def bb_plot(
    df: pd.DataFrame, 
    cov1: str = None, 
    cov2: str = None,
    title: bool = False,
    show_y: bool = True, 
    categorical_cmap: str|Dict[str,Any] = 'tab10', 
    ax: matplotlib.axes.Axes = None, 
    ) -> matplotlib.axes.Axes:
    """
    Stacked composition plot.
    """

    # Prep data
    df[cov1] = pd.Categorical(df[cov1]).remove_unused_categories()
    df[cov2] = pd.Categorical(df[cov2]).remove_unused_categories()
    data = pd.crosstab(df[cov1], df[cov2], normalize='index')
    data_cum = data.cumsum(axis=1)
    ys = data.index.categories
    labels = data.columns.categories

    # Ax
    _cmap = None
    if isinstance(categorical_cmap, str):
        _cmap = create_palette(df, cov2, palette=categorical_cmap)
    elif isinstance(categorical_cmap, dict):
        _cmap = categorical_cmap
        assert all([ x in _cmap for x in df[cov2].unique() ])
    else:
        raise ValueError('Provide either a dict or str for categorical_cmap!')
        
    for i, x in enumerate(labels):
        widths = data.values[:,i]
        starts = data_cum.values[:,i] - widths
        ax.barh(ys, widths, left=starts, height=0.95, label=x, color=_cmap[x])

    # Format
    ax.set_xlim(-0.01, 1.01)
    format_ax(
        ax, 
        title = f'{cov1} by {cov2}' if title else '',
        yticks='' if not show_y else ys, 
        xlabel='Abundance %'
    )
    
    return ax
    

##


def rank_plot(df, cov=None, ascending=False, n_annotated=25, title=None,
            ylabel=None, ax=None, fig=None):
    """
    Annotated scatterplot.
    """
    s = df[cov].sort_values(ascending=ascending)
    x = np.arange(df.shape[0])
    y = s.values
    labels = s[:n_annotated].index
    ax.plot(x, y, '.')
    ta.allocate_text(fig, ax, x[:n_annotated], y[:n_annotated], labels, x_scatter=x, y_scatter=y,
        linecolor='black', textsize=8, max_distance=0.5, linewidth=0.5, nbr_candidates=100)
    format_ax(ax, title=title, xlabel='rank', ylabel=ylabel)

    return ax


##
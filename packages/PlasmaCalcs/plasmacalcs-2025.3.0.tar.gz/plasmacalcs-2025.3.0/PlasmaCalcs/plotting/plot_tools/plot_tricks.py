"""
File Purpose: misc tricks related to plotting

stuff that's sometimes easy to forget, but super useful if you remember it.
"""

import matplotlib.pyplot as plt

def ax_outline(ax=None, *, color='black', linewidth=1):
    '''draw a box around the axes'''
    if ax is None:
        ax = plt.gca()
    ax.patch.set(linewidth=linewidth, edgecolor=color)

def fig_outline(fig=None, *, color='red', linewidth=1):
    '''draw a box around the figure'''
    if fig is None:
        fig = plt.gcf()
    fig.patch.set(linewidth=linewidth, edgecolor=color)

def ax_remove_ticks(ax=None):
    '''remove ticks from the axes!'''
    if ax is None:
        ax = plt.gca()
    ax.set(xticks=[], yticks=[])

def ax_remove_ticklabels(ax=None):
    '''remove ticklabels from the axes (but don't remove ticks)!'''
    if ax is None:
        ax = plt.gca()
    ax.set(xticklabels=[], yticklabels=[])

def get_min_n_ticks(ax=None):
    '''get the minimum number of ticks on this axes (current axes if None provided).
    This "minimum" is according to the x and y tick locators.
    Returns (min for x-axis, min for y-axis).
    None if cannot find tick locator with a minimum number of ticks.
    '''
    if ax is None:
        ax = plt.gca()
    ticker_x = ax.xaxis.get_major_locator()
    if hasattr(ticker_x, 'base'):  # e.g., RadialLocator or ThetaLocator
        ticker_x = ticker_x.base
    result_x = getattr(ticker_x, '_min_n_ticks', None)
    ticker_y = ax.yaxis.get_major_locator()
    if hasattr(ticker_y, 'base'):
        ticker_y = ticker_y.base
    result_y = getattr(ticker_y, '_min_n_ticks', None)
    return (result_x, result_y)

def set_min_n_ticks(n, ax=None, *, fail_ok=True):
    '''set the minimum number of ticks on this axes (current axes if None provided).
    Alters the tick locators for x and y axes here, via locator.set_params(min_n_ticks=n)
    If tick locators have 'base', use locator.base.set_params(min_n_ticks=n) instead.
        (e.g. RadialLocator and ThetaLocator have 'base'.)

    n: int or 2-tuple of ints
        minimum number of ticks to have on the x, y axes.
        single int --> equivalent to providing (n, n).
    fail_ok: bool
        whether it is okay to fail silently if not able to set min_n_ticks in the existing locators.

    returns (whether succeeded for x-axis, whether succeeded for y-axis)
    '''
    if ax is None:
        ax = plt.gca()
    try:
        iter(n)
    except TypeError:
        n = (n,n)
    nx, ny = n
    # x axis
    ticker_x = ax.xaxis.get_major_locator()
    if hasattr(ticker_x, 'base'):  # e.g., RadialLocator or ThetaLocator
        ticker_x = ticker_x.base
    try:
        ticker_x.set_params(min_n_ticks=nx)
    except Exception:  # not BaseException! e.g., don't catch KeyboardInterrupt.
        success_x = False
        if not fail_ok:
            raise
    else:
        success_x = True
    # y axis
    ticker_y = ax.yaxis.get_major_locator()
    if hasattr(ticker_y, 'base'):
        ticker_y = ticker_y.base
    try:
        ticker_y.set_params(min_n_ticks=ny)
    except Exception:
        success_y = False
        if not fail_ok:
            raise
    else:
        success_y = True
    return (success_x, success_y)


# # size of a drawn artist (e.g., textbox, axes...) # #
# artist.get_window_extent()

# # actual aspect ratio of an axes # #
def ax_aspect(ax):
    # Total figure size
    figW, figH = ax.get_figure().get_size_inches()
    # Axis size on figure
    _, _, w, h = ax.get_position().bounds
    # Ratio of display units
    disp_ratio = (figH * h) / (figW * w)
    # Ratio of data units
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    data_ratio = (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
    return disp_ratio / data_ratio

# # convenient locations to have for reference: # # 
PLOT_LOCATION_NAMES = \
    ''''outer upper left',    'above upper left', 'above upper center', 'above upper right', 'outer upper right',
    'outside upper left',  'upper left',       'upper center',       'upper right',       'outside upper right',
    'outside center left', 'center left',      'center',             'center right',      'outside center right',
    'outside lower left',  'lower left',       'lower center',       'lower right',       'outside lower right',
    'outer lower left',    'below lower left', 'below lower center', 'below lower right', 'outer lower right'.'''

def plot_locations(margin=0.03):
    '''dict of xy=(x,y) in axes coordinates (0=left/bottom, 1=right/top) for various locations;
    also includes nice values for ha & va to use for aligning text.

    margin: number, probably between 0 and 0.25
        margin to add to the plot locations. E.g. use 0+margin for bottom instead of 0.

    The locations are as follows, with outer/above/outside/below referring to locations outside the axes.
    'outer upper left',    'above upper left', 'above upper center', 'above upper right', 'outer upper right',
    'outside upper left',  'upper left',       'upper center',       'upper right',       'outside upper right',
    'outside center left', 'center left',      'center',             'center right',      'outside center right',
    'outside lower left',  'lower left',       'lower center',       'lower right',       'outside lower right',
    'outer lower left',    'below lower left', 'below lower center', 'below lower right', 'outer lower right'.
    '''
    result = {
        # inside the axes:
        'upper left':   dict(xy=(0+margin, 1-margin), ha='left',   va='top'),
        'upper center': dict(xy=(0.5     , 1-margin), ha='center', va='top'),
        'upper right':  dict(xy=(1-margin, 1-margin), ha='right',  va='top'),
        'center left':  dict(xy=(0+margin, 0.5     ), ha='left',   va='center'),
        'center':       dict(xy=(0.5     , 0.5     ), ha='center', va='center'),
        'center right': dict(xy=(1-margin, 0.5     ), ha='right',  va='center'),
        'lower left':   dict(xy=(0+margin, 0+margin), ha='left',   va='bottom'),
        'lower center': dict(xy=(0.5     , 0+margin), ha='center', va='bottom'),
        'lower right':  dict(xy=(1-margin, 0+margin), ha='right',  va='bottom'),
        # outside the axes - top row:
        'outer upper left':     dict(xy=(0-margin, 1+margin), ha='right',  va='bottom'),
        'above upper left':     dict(xy=(0+margin, 1+margin), ha='left',   va='bottom'),
        'above upper center':   dict(xy=(0.5     , 1+margin), ha='center', va='bottom'),
        'above upper right':    dict(xy=(1-margin, 1+margin), ha='right',  va='bottom'),
        'outer upper right':    dict(xy=(1+margin, 1+margin), ha='left',   va='bottom'),
        # outside the axes - left & right columns
        'outside upper left':   dict(xy=(0-margin, 1-margin), ha='right',  va='top'),
        'outside upper right':  dict(xy=(1+margin, 1-margin), ha='left',   va='top'),
        'outside center left':  dict(xy=(0-margin, 0.5     ), ha='right',  va='center'),
        'outside center right': dict(xy=(1+margin, 0.5     ), ha='left',   va='center'),
        'outside lower left':   dict(xy=(0-margin, 0+margin), ha='right',  va='bottom'),
        'outside lower right':  dict(xy=(1+margin, 0+margin), ha='left',   va='bottom'),
        # outside the axes - bottom row:
        'outer lower left':     dict(xy=(0-margin, 0-margin), ha='right',  va='top'),
        'below lower left':     dict(xy=(0+margin, 0-margin), ha='left',   va='top'),
        'below lower center':   dict(xy=(0.5     , 0-margin), ha='center', va='top'),
        'below lower right':    dict(xy=(1-margin, 0-margin), ha='right',  va='top'),
        'outer lower right':    dict(xy=(1+margin, 0-margin), ha='left',   va='top'),
        }
    return result

def plot_note(note, xy='upper left', *, margin=0.03, **kw_annotate):
    '''add this note to the current plot at the indicated position.
    For more detailed control, use plt.annotate instead.

    xy: str or tuple
        position in axes coords.
        str -> also sets horizontal & vertical alignment (via 'ha' & 'va' kwargs).
        See below for valid strings.
    margin: number, probably between 0 and 0.25
        margin to add to the plot locations. E.g. use 0+margin for bottom instead of 0.

    Valid strings are (with outer/above/outside/below being outside the axes):
    'outer upper left',    'above upper left', 'above upper center', 'above upper right', 'outer upper right',
    'outside upper left',  'upper left',       'upper center',       'upper right',       'outside upper right',
    'outside center left', 'center left',      'center',             'center right',      'outside center right',
    'outside lower left',  'lower left',       'lower center',       'lower right',       'outside lower right',
    'outer lower left',    'below lower left', 'below lower center', 'below lower right', 'outer lower right'.
    '''
    defaults = plot_locations(margin=margin)
    if isinstance(xy, str):
        if xy not in defaults:
            raise ValueError(f"Invalid xy string: {xy!r}. Expected one of:\n    {PLOT_LOCATION_NAMES}")
        kw_annotate = {**defaults[xy], **kw_annotate}
    else:
        kw_annotate['xy'] = xy
    kw_annotate.setdefault('xycoords', 'axes fraction')
    return plt.annotate(note, **kw_annotate)

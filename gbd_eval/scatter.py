# MIT License
#
# © 2023 Markus Iser, University of Helsinki
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# run: ./eval.py


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from gbd_eval.util import name


def matplotlib_export_fix_compatiblity():
    matplotlib.use('GTK3Agg')

def matplotlib_export_pgf():
    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
    })

def plt_decorate_scatter_area(min=0, max=5000):
    plt.axline((0, 0), (1, 1), linewidth=0.5, color='lightgrey', zorder=0)
    plt.axhline(y=max, xmin=min, xmax=max, linewidth=0.5, color='lightgrey', zorder=0)
    plt.axvline(x=max, ymin=min, ymax=max, linewidth=0.5, color='lightgrey', zorder=0)
    plt.axhline(y=min, xmin=min, xmax=max, linewidth=0.5, color='lightgrey', zorder=0)
    plt.axvline(x=min, ymin=min, ymax=max, linewidth=0.5, color='lightgrey', zorder=0)
    plt.xticks(list(np.arange(min, max, (max - min) / 10)) + [max])
    plt.yticks(list(np.arange(min, max, (max - min) / 10)) + [max])

def export_legend(legend, filename="legend.pdf"):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    #bbox = bbox.from_extents(*(bbox.extents + np.array([0.05, .25, -0.05, -0.02])))
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)

def depenalize(df: pd.DataFrame, solvers: list[str], max=5000):
    for name in solvers:
        df.loc[df[name] > max, name] = max
    return df

def scatter(df: pd.DataFrame, solver1, solver2, groupcol, title=None, max=5000, legend_separate=None, to_latex=None, logscale=False, print_delta=False):
    colors = ['#113377','#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#a65628']
    markers = [ '1', 'x', '*', '+', '.' ]
    fig, ax = plt.subplots(figsize=(3.5,3.5))
    plt_decorate_scatter_area(min=0, max=max)
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.tick_params(axis='both', which='minor', labelsize=6)
    plt.xlabel(name(solver1), fontsize=9)
    plt.ylabel(name(solver2), fontsize=9)
    if logscale:
        ax.set_xscale('log', base=10)
        ax.set_yscale('log', base=10)
    else:
        plt.xticks(rotation=45)
    # remove spines:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # sort group by score difference
    gf = df.groupby(groupcol).mean(numeric_only=True).reset_index()
    gf["diff"] = gf[solver1] - gf[solver2]
    gf["adiff"] = gf["diff"].abs()
    gf.sort_values(by='adiff', ascending=False, inplace=True)

    df = depenalize(df.copy(), [solver1, solver2], max)

    for i, group in enumerate(gf[groupcol], 0):
        m = markers[i % len(markers)]
        c = colors[i % len(colors)]
        fdf = df.loc[df[groupcol] == group]
        gdelta = "{:.2f}".format(gf.loc[gf[groupcol] == group]["diff"].values[0])
        title = name(group)
        if print_delta:
            title = title + " ($\Delta_{xy}=$" + gdelta + ")"
        ax.scatter(fdf[solver1], fdf[solver2], color=c, marker=m, s=30, alpha=.7, linewidth=.7, zorder=i, label=title)

    ax.set_aspect('equal', 'box')
    lege = ax.legend(loc='center left', bbox_to_anchor=(1.0, .5), ncol=1, frameon=False, fontsize='xx-small', borderaxespad=0, columnspacing=0, labelspacing=.3)
    
    if legend_separate is not None:
        export_legend(lege, legend_separate)
        lege.remove()

    if to_latex is None:
        plt.show()
    else:
        plt.savefig(to_latex, bbox_inches='tight', pad_inches=0.1)

    plt.close()
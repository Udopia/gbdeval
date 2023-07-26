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

import pandas as pd
import matplotlib.pyplot as plt

from gbd_eval.scatter import export_legend
from gbd_eval.util import name


def plt_decorate_cactus_plot_area(num=400, min=0, max=5000, holy=False):
    plt.grid(linestyle='dashed', linewidth=.5, color='lightgrey', zorder=0)
    if holy:
        plt.xlim(0, num)
        plt.ylim(min, max + (max - min) / 100)
    else:
        plt.xlim(min, max + (max - min) / 100)
        plt.ylim(0, num)


def cactus(df: pd.DataFrame, solvers: list[str], title=None, num=17, max=5000, legend_separate=None, to_latex=None, holy=True):
    colors = ['#113377','#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#a65628']
    markers = [ '1', 'x', '*', '+', '.' ]

    fig, ax = plt.subplots(figsize=(3.5,3.5))

    plt_decorate_cactus_plot_area(len(df.index), min=0, max=max, holy=holy)
    if title is not None:
        ax.set_title(title, fontsize=6, variant='small-caps')
    # remove spines:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    df2 = pd.concat([df[col].sort_values(ascending=True, ignore_index=True) for col in solvers], axis=1)
    avg = df2.mean(numeric_only=True)
    solvers.sort(key=lambda x: avg[x])


    k = 1 if to_latex is not None else 2
    
    lines = []
    for i, col in enumerate(solvers[:num], 0):
        m = markers[i % len(markers)]
        c = colors[i % len(colors)]
        o = len(solvers) - i
        line = ax.plot(df2[col], label=name(col), zorder=o, marker=m, color=c, fillstyle='none', alpha=.7, linewidth=.5*k, markeredgewidth=.5*k, markersize=3*k, drawstyle='steps-post')
        lines.append(line[0])

    lege = plt.legend(loc='center left', bbox_to_anchor=(1.0, .5), ncol=1, frameon=False, fontsize='x-small', borderaxespad=1.5, columnspacing=0, labelspacing=.7)

    if legend_separate is not None:
        export_legend(lege, legend_separate)
        lege.remove()

    if not holy:
        for line in lines:
            xdata, ydata = line.get_xdata(), line.get_ydata()
            line.set_xdata(ydata)
            line.set_ydata(xdata)
        ax.set_aspect(max / len(df2.index))
    else:
        ax.set_aspect(len(df2.index) / max)

    if to_latex is None:
        plt.show()
    else:
        plt.savefig(to_latex, bbox_inches='tight', pad_inches=0.1)

    plt.close()


def cdf(df: pd.DataFrame, solvers: list[str], title=None, num=17, max=5000, legend_separate=None, to_latex=None):
    cactus(df, solvers=solvers, title=title, num=num, max=max, legend_separate=legend_separate, to_latex=to_latex, holy=False)


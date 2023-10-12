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

from gbd_eval.util import name, number


def table(df: pd.DataFrame, solvers: list[str], groups: list[str], to_latex: str, bold_min_of: list[str] = None, min_diff=0):
    df["diff"] = df[solvers].max(axis=1) - df[solvers].min(axis=1)
    df = df.query("diff >= @min_diff").copy()
    df.drop(columns=["diff"], inplace=True)
    s = df.style.format(precision=2, subset=solvers)
    s.hide(axis="index")
    s = s.format(name, subset=groups)
    s = s.format(number, subset=solvers)
    s = s.format_index(name, axis=1)
    if bold_min_of is not None:
        s = s.highlight_min(axis=1, subset=bold_min_of, props='bfseries: ;')
    sformat = "r"
    width = "{:.2f}".format(.6 / len(solvers))
    sformat = ">{\\raggedleft\\arraybackslash}p{" + width + "\linewidth}"
    s.to_latex(to_latex, hrules=True, clines="all;data", column_format="l" * len(groups) + "r|" + sformat * (len(solvers)-1) + "|" + sformat)


def portfolios(df: pd.DataFrame, to_latex: str):
    s = df.style.format(precision=2, subset=["score"])
    s.hide(axis="index")
    s = s.format_index(name, axis=1)
    s.to_latex(to_latex, hrules=True, clines="all;data", column_format="l|p{.9\linewidth}|r")
    return df

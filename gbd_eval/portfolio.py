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
from itertools import combinations
from gbd_eval import tables
from gbd_eval.util import name

def pscore(df: pd.DataFrame, solvers: list[str]):
    return df[solvers].min(axis=1).mean()

def pscores_all(df: pd.DataFrame, solvers: list[str], k: int):
    return sorted([ (comb, pscore(df, list(comb))) for comb in combinations(solvers, k) ], key=lambda k : k[1])

def pscores_ext(df: pd.DataFrame, solvers: list[str], tuples: list[tuple[str]]):
    tupset = set(frozenset(comb + (s,)) for comb in tuples for s in solvers if s not in comb)
    return sorted([ (tuple(comb), pscore(df, list(comb))) for comb in tupset ], key=lambda k : k[1])

def generate_portfolios(df: pd.DataFrame, solvers: list[str], max_k: int = 3, width: int = 10):
    pfs = [ pscores_all(df, solvers, 1)[:width], pscores_all(df, solvers, 2)[:width] ]
    for _ in range(3, max_k):
        pfs.append(pscores_ext(df, solvers, [p[0] for p in pfs[-1]])[:width])
    # sort solvers in tuples by occurence in portfolios:
    occ = { s: [ t for pf in pfs for p in pf for t in p[0] ].count(s) for s in solvers }
    pfs = [ [ (tuple(sorted(p[0], key=lambda s : occ[s], reverse=True)), p[1]) for p in pf ] for pf in pfs ]
    return pfs


def portfolios(df: pd.DataFrame, solvers: list[str], max_k: int = 8, max_size=3, width: int = 10, to_latex: str = None):
    pfs = generate_portfolios(df, solvers, max_k, width)
    structured = { (len(tup), ", ".join([name(t) for t in tup])): score for portfolios in pfs for (tup, score) in portfolios[:max_size] }
    df = pd.DataFrame(structured, index=["score"]).transpose()
    df.index.names = ["k", "portfolio"]
    df.reset_index(inplace=True)
    s = df.style.format(precision=2, subset=["score"])
    s.hide(axis="index")
    #s = s.format(tables.column4latex, subset=["portfolio"])
    s = s.format_index(tables.header4latex, axis=1)
    s.to_latex(to_latex, hrules=True, clines="all;data", column_format="l|p{.9\linewidth}r")
    return df

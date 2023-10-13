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
from gbd_eval.preprocess import DataPreprocessor

def pscore(df: pd.DataFrame, solvers: list[str]):
    return df[solvers].min(axis=1).mean()

def pscores_all(df: pd.DataFrame, solvers: list[str], k: int):
    return sorted([ (comb, pscore(df, list(comb))) for comb in combinations(solvers, k) ], key=lambda k : k[1])

def pscores_ext(df: pd.DataFrame, solvers: list[str], tuples: list[tuple[str]]):
    tupset = set(frozenset(comb + (s,)) for comb in tuples for s in solvers if s not in comb)
    return sorted([ (tuple(comb), pscore(df, list(comb))) for comb in tupset ], key=lambda k : k[1])

class Portfolios:

    def __init__(self, gbd, query, solvers, max_runtime: int = 5000):
        self.gbd = gbd
        self.query = query
        self.solvers = solvers
        self.df = DataPreprocessor(gbd, query, solvers).numeric(solvers).penalize(solvers, max_runtime).get()
        self.pfs = []
        self.max_runtime = max_runtime

    def generate(self, max_k: int = 3, beam_width: int = 10):
        self.pfs = [ pscores_all(self.df, self.solvers, 1)[:beam_width] ]
        self.pfs.append(pscores_all(self.df, self.solvers, 2)[:beam_width])
        for _ in range(3, max_k):
            self.pfs.append(pscores_ext(self.df, self.solvers, [p[0] for p in self.pfs[-1]])[:beam_width])
        return self
    
    def sorted(self):
        # sort solvers in tuples by occurence in portfolios:
        occ = { s: [ t for pf in self.pfs for p in pf for t in p[0] ].count(s) for s in self.solvers }
        self.pfs = [ [ (tuple(sorted(p[0], key=lambda s : occ[s], reverse=True)), p[1]) for p in pf ] for pf in self.pfs ]
        return self

    def get(self, n_best: int = 3, rename = lambda s : s):
        structured = { (len(tup), ",".join([rename(t) for t in tup])): score for portfolios in self.pfs for (tup, score) in portfolios[:n_best] }
        df = pd.DataFrame(structured, index=["score"]).transpose()
        df.index.names = ["k", "portfolio"]
        df.reset_index(inplace=True)
        return df
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

def get_portfolio_scores(df: pd.DataFrame, solvers: list[str], k: int):
    return [ (str(list(comb)), df[list(comb)].min(axis=1).mean()) for comb in combinations(solvers, k) ]

def portfolios(df: pd.DataFrame, solvers: list[str], max_k: int, width: int = 10):
    for k in range(1, max_k+1):
        print(get_portfolio_scores(df, solvers, k))
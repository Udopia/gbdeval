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


def escape4latex(val):
    return val.replace("_", "\\_")

def column4latex(val):
    names = {
        "all": "\hline All",
    }
    if val in names:
        return names[val]
    else:
        return escape4latex(val).title()
    
def header4latex(val):
    names = {
        "vbs": "VBS",
        "SBVA_sbva_cadical": "SBVA CaDiCaL",
        "SBVA_sbva_kissat": "SBVA Kissat",
    }
    if val in names:
        return names[val]
    else:
        return escape4latex(val).title()


def table(df: pd.DataFrame, solvers: list[str], groups: list[str], to_latex: str,          
          bold_min_of: list[str] = None):
    s = df.style.format(precision=2, subset=solvers)
    s.hide(axis="index")
    s = s.format(column4latex, subset=groups).format_index(header4latex, axis=1)
    if bold_min_of is not None:
        s = s.highlight_min(axis=1, subset=bold_min_of, props='bfseries: ;')
    s.to_latex(to_latex, hrules=True, clines="all;data", 
               column_format="l" * len(groups) + "r|" + "c" * (len(solvers)-1) + "|c")

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


def scores(df: pd.DataFrame):
    return df.mean(numeric_only=True).to_frame().transpose()

    
def scores_group_wise(df: pd.DataFrame, solvers: list[str], groups: list[str]):
    #group:
    counts = df.groupby('family').count()["hash"].rename("count")
    groups = df.groupby('family').mean(numeric_only=True)
    tab = groups.merge(counts, on='family', how='left')
    tab.reset_index(inplace=True)
    #reorder:
    tab = tab[["family", "count"] + solvers + ["vbs"]]
    tab.sort_values(by='count', ascending=False, inplace=True)
    #add all:
    all = scores(df)
    all["family"] = "all"
    all["count"] = len(df.index)    
    tab = pd.concat([tab, all], ignore_index=True)
    return tab
# Evaluation Demo

In the following, we use the benchmark instance labels provided by GBD's meta.db, and the solver runtimes in the 2023 SAT competition.



```python
from gbd_core.api import GBD
import pandas as pd

def get_solvers():
    with GBD(['data/sc2023/results_main_detailed.csv']) as gbd:
        return [ s for s in gbd.get_features() if s not in ["aresult", "vresult"] ]

def get_sc23_data(runtimes, metadata, addvbs=False):
    with GBD(['data/meta.db', 'data/sc2023/results_main_detailed.csv']) as gbd:
        df = gbd.query("track=main_2023", resolve=runtimes + metadata, collapse='min')
        # convert runtimes to numeric values
        df[runtimes] = df[runtimes].apply(pd.to_numeric)
        # penalize timeouts
        for solver in runtimes:
            df.loc[df[solver] >= 5000, solver] = 10000
        if addvbs:
            # compute the vbs score
            df["vbs"] = df[runtimes].min(axis=1)
        return df
```

### Portfolio Analysis

Next, we determine the best 3-portfolio of solvers in the 2023 SAT competition.


```python
from itertools import combinations

def pscore(df: pd.DataFrame, solvers: list[str]):
    return df[solvers].min(axis=1).mean()

def pscores_all(df: pd.DataFrame, solvers: list[str], k: int):
    return sorted([ (comb, pscore(df, list(comb))) for comb in combinations(solvers, k) ], key=lambda k : k[1])

def pscores_ext(df: pd.DataFrame, solvers: list[str], tuples: list[tuple[str]]):
    tupset = set(frozenset(comb + (s,)) for comb in tuples for s in solvers if s not in comb)
    return sorted([ (tuple(comb), pscore(df, list(comb))) for comb in tupset ], key=lambda k : k[1])

beam_width: int = 10
pf3 = get_solvers()
runtimes = get_sc23_data(pf3, [])
pfs1 = pscores_all(runtimes, pf3, 1)
pfs2 = pscores_all(runtimes, pf3, 2)[:beam_width]
pfs3 = pscores_ext(runtimes, pf3, [tup[0] for tup in pfs2])[:beam_width]

pf1, pf1score = list(pfs1[0][0]), round(pfs1[0][1], 2)
pf2, pf2score = list(pfs2[0][0]), round(pfs2[0][1], 2)
pf3, pf3score = list(pfs3[0][0]), round(pfs3[0][1], 2)

print("Single-best Solver and Best 2- and 3-Portfolios")
print(pf1score, pf1)
ordered = [ s[0][0] for s in pfs1 ]
print(pf2score, sorted(pf2, key=lambda s : ordered.index(s)))
print(pf3score, sorted(pf3, key=lambda s : ordered.index(s)))
```

    Single-best Solver and Best 2- and 3-Portfolios
    3274.01 ['SBVA_sbva_cadical']
    2434.72 ['SBVA_sbva_cadical', 'Kissat_MAB_prop_pr_no_sym']
    2138.96 ['SBVA_sbva_cadical', 'Kissat_MAB_prop_pr_no_sym', 'BreakID_kissat_low_sh']


### Category-wise Ranking

Determine the PAR-2 scores per instance category for each solver in the best 3-portfolio.


```python
df = get_sc23_data(pf3, ["family"])
# group families with less than 5 instances into a single group
misc = df.groupby("family").count().query("hash < 5").index.tolist()
df.replace(misc, "miscellaneous", inplace=True)
# compute family sizes and family-wise scores
counts = df.groupby('family').count()["hash"].rename("count")
groups = df.groupby('family').mean(numeric_only=True)
tab = groups.merge(counts, on='family', how='left').reset_index()
# sort families by the difference between the best and worst solver
tab["diff"] = tab[pf3].max(axis=1) - tab[pf3].min(axis=1)
tab.sort_values(by="diff", ascending=False, inplace=True)
tab = tab[["family", "count"] + pf3].reset_index(drop=True)
tab.to_markdown("family_scores.md", index=False, floatfmt=".2f")
# output family_scores.md
with open("family_scores.md", "r") as f:
    print(f.read())
```

    | family                       |   count |   Kissat_MAB_prop_pr_no_sym |   SBVA_sbva_cadical |   BreakID_kissat_low_sh |
    |:-----------------------------|--------:|----------------------------:|--------------------:|------------------------:|
    | interval-matching            |      20 |                        0.15 |            10000.00 |                10000.00 |
    | or_randxor                   |       5 |                    10000.00 |               21.82 |                  103.93 |
    | hashtable-safety             |      20 |                      194.75 |              797.46 |                10000.00 |
    | satcoin                      |      15 |                    10000.00 |             1395.53 |                10000.00 |
    | set-covering                 |      20 |                     5761.57 |              722.01 |                  262.39 |
    | cryptography-ascon           |      20 |                     5628.35 |              356.82 |                 2673.77 |
    | grs-fp-comm                  |      17 |                     3435.82 |             3649.90 |                 8258.64 |
    | reg-n                        |       5 |                     6295.16 |            10000.00 |                10000.00 |
    | mutilated-chessboard         |      12 |                     1656.50 |             3194.54 |                 5135.77 |
    | profitable-robust-production |      20 |                     3946.63 |             2470.42 |                 5031.37 |
    | hardware-verification        |       8 |                     1558.52 |             2832.05 |                 3964.51 |
    | register-allocation          |      20 |                        5.50 |              101.20 |                 2016.39 |
    | tseitin                      |      11 |                     8193.40 |             8196.91 |                 6393.20 |
    | social-golfer                |      20 |                     7665.62 |             7555.16 |                 9013.05 |
    | miscellaneous                |      70 |                     2563.98 |             3164.75 |                 3918.52 |
    | pigeon-hole                  |       8 |                     6381.16 |             5261.85 |                 5128.03 |
    | school-timetabling           |      19 |                     1266.09 |             1399.65 |                 2371.42 |
    | brent-equations              |      19 |                      408.33 |              232.86 |                 1133.50 |
    | miter                        |      11 |                     3157.68 |             3134.91 |                 3723.05 |
    | argumentation                |      20 |                     4144.27 |             3693.93 |                 3820.58 |
    | subsumptiontest              |       5 |                       84.60 |              230.22 |                   89.14 |
    | planning                     |       6 |                       91.26 |                6.97 |                   10.98 |
    | quasigroup-completion        |       5 |                       60.78 |                9.33 |                    3.43 |
    | cryptography                 |       7 |                     1577.96 |             1578.46 |                 1570.64 |
    | cryptography-simon           |      17 |                    10000.00 |            10000.00 |                10000.00 |


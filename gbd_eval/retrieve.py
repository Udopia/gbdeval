# MIT License

# © 2023 Markus Iser, University of Helsinki

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

from gbd_core.api import GBD
import pandas as pd


# retrieve solver runtimes and instance features from GBD
def retrieve_augmented_runtimes(gbd: GBD, solvers: list[str], features: list[str] = [], query: str = None):
    df = gbd.query(query, resolve=features + solvers)
    for name in solvers:
        df[name] = pd.to_numeric(df[name], errors='coerce')
    return df


def penalize_small_groups(df: pd.DataFrame, features: list[str] = ["family"], min_count: int = 5):
    for group in features:
        small = df.groupby(group).count().query("hash < {}".format(min_count)).index.tolist()
        small.extend(["empty", "unknown"])
        df.replace(small, "miscellaneous", inplace=True)
    return df


def penalize_runtimes(df: pd.DataFrame, solvers: list[str], max=5000, p=2):
    for name in solvers:
        df.loc[df[name] >= max, name] = p*max
        df.loc[df[name] < 0, name] = p*max # penalize negative values as well (treated as error states)
    return df


def retrieve_penalized_augmented_runtimes(gbd: GBD, solvers: list[str], features: list[str] = ["family"], query: str = None, max_runtime: int = 5000, min_group_size: int = 5):
    df = retrieve_augmented_runtimes(gbd, solvers, features, query)
    df = penalize_small_groups(df, features, min_count=min_group_size)
    df = penalize_runtimes(df, solvers, max=max_runtime)
    return df


def retrieve_virtual_best_solver(gbd: GBD, solvers: list[str], query: str = None):
    df = retrieve_augmented_runtimes(gbd, solvers, [], query)
    for name in solvers:
        df[name] = pd.to_numeric(df[name], errors='coerce')
    df["vbs"] = df[solvers].min(axis=1)
    return df.drop(solvers, axis=1)
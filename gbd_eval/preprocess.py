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

class DataPreprocessor:

    def __init__(self, gbd: GBD, query: str, features: list[str]):
        self.gbd = gbd
        self.query = query
        self.features = features
        self.df = gbd.query(query, resolve=features)

    def get(self):
        return self.df

    def numeric(self, columns: list[str]):
        for name in columns:
            self.df[name] = pd.to_numeric(self.df[name], errors='coerce')
        return self
    
    def penalize(self, columns: list[str], max_runtime: int = 5000):
        for name in columns:
            self.df.loc[self.df[name] >= max_runtime, name] = 2*max_runtime
            self.df.loc[self.df[name] < 0, name] = 2*max_runtime
        return self

    def remainder(self, column: str, min_group_size: int = 5, rname: str = "miscellaneous"):
        small = self.df.groupby(column).count().query("hash < {}".format(min_group_size)).index.tolist()
        small.extend(["empty", "unknown"])
        self.df.replace(small, rname, inplace=True)
        return self
    
    def vbs(self, columns: list[str]):
        if set(columns) <= set(self.df.columns):
            self.df["vbs"] = self.df[columns].min(axis=1)
        else:
            data = DataPreprocessor(self.gbd, self.query, columns)
            vbs = data.numeric(columns).penalize(columns).vbs(columns).get()
            self.df["vbs"] = vbs[columns].min(axis=1)
        return self

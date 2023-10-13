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

#!/usr/bin/python3
# run: ./eval.py

import os
import itertools

from gbd_core.api import GBD
from gbd_eval import scatter, cactus, scores, tables, util
from gbd_eval.preprocess import DataPreprocessor
from gbd_eval.portfolio import Portfolios


class Generator:

    def __init__(self, query: str, dbs: list[str], solvers: list[str], target_dir: str, timeout: int = 5000):
        self.query = query
        self.gbd = GBD(dbs)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        self.target_dir = target_dir
        self.solvers = solvers
        self.max_runtime = timeout

    def get_solvers(self):
        return self.solvers

    def generate_cdf_plot(self):
        data = DataPreprocessor(self.gbd, self.query, self.solvers)
        df = data.numeric(self.solvers).penalize(self.solvers, self.max_runtime).vbs(self.solvers).get()
        cactus.cactus(df.copy(), self.solvers + ["vbs"], holy=False, max=self.max_runtime, to_latex="{}/cdf.pdf".format(self.target_dir))

    def generate_cactus_plot(self):
        data = DataPreprocessor(self.gbd, self.query, self.solvers)
        df = data.numeric(self.solvers).penalize(self.solvers, self.max_runtime).vbs(self.solvers).get()
        cactus.cactus(df.copy(), self.solvers + ["vbs"], holy=True, max=self.max_runtime, to_latex="{}/cactus.pdf".format(self.target_dir))

    def generate_scatter_plot(self, s0: str, s1: str, name: str):
        data = DataPreprocessor(self.gbd, self.query, [s0, s1, "family"])
        df = data.numeric([s0, s1]).penalize([s0, s1], self.max_runtime).remainder("family").get()
        scatter.scatter(df, s0, s1, "family", max=self.max_runtime, logscale=False, to_latex="{}/{}.pdf".format(self.target_dir, name))
        scatter.scatter(df, s0, s1, "family", max=self.max_runtime, logscale=True, to_latex="{}/{}_logscale.pdf".format(self.target_dir, name))

    def generate_family_wise_score_table(self, solvers: list[str], name: str, vbs_from: list[str] = None):
        data = DataPreprocessor(self.gbd, self.query, solvers + ["family"])
        df = data.numeric(solvers).penalize(solvers, self.max_runtime).remainder("family").vbs(vbs_from or solvers).get()
        tab = scores.scores_group_wise(df, solvers, ["family"], sortby="diff")
        tables.table(tab, solvers + [ "vbs" ], ["family"], "{}/{}.tex".format(self.target_dir, name), bold_min_of=solvers, min_diff=200)
    
    def generate_cdf_per_family(self):
        data = DataPreprocessor(self.gbd, self.query, self.solvers + ["family"])
        df = data.numeric(self.solvers).penalize(self.solvers, self.max_runtime).remainder("family").vbs(self.solvers).get()
        for fam in df["family"].unique():
            subdf = df.query("family == '{}'".format(fam))
            cactus.cdf(subdf, self.solvers, title=fam, num=7, max=self.max_runtime,
                        #legend_separate="gen/sc2023/cdfs/leg-{}.pdf".format(fam), 
                        to_latex="{}/cdf-{}.pdf".format(self.target_dir, fam))
        
    def generate_portfolios_table(self):
        pfgen = Portfolios(self.gbd, self.query, self.solvers, self.max_runtime)
        pfs = pfgen.generate(max_k=4, beam_width=10).sorted().get(n_best=3, rename=util.name)
        tables.portfolios(pfs, "{}/portfolios.tex".format(self.target_dir))

    def get_best_portfolio(self, size: int = 3):
        pfgen = Portfolios(self.gbd, self.query, self.solvers, self.max_runtime)
        pfs = pfgen.generate(max_k=size+1, beam_width=10).sorted().get(n_best=1)
        return pfs.query("k == {}".format(size))["portfolio"].values[0].split(",")


def generate():
    tracks = {
        "main": {
            "files": ['data/meta.db', 'data/sc2023/results_main_detailed.csv'],
            "timeout": 5000,
            "solvers": [],
        },
        "special": {
            "files": ['data/meta.db', 'data/sc2023/results_special_detailed.csv'],
            "timeout": 5000,
            "solvers": [],
        },
        "parallel": {
            "files": ['data/meta.db', 'data/sc2023/results_parallel_detailed.csv'],
            "timeout": 5000,
            "solvers": [],
        },
        "cloud": {
            "files": ['data/meta.db', 'data/sc2023/results_cloud_detailed.csv'],
            "timeout": 1000,
            "solvers": [],
        },
        "main-parallel": {
            "files": ['data/meta.db', 'data/sc2023/results_main_detailed.csv', 'data/sc2023/results_parallel_detailed.csv'],
            "timeout": 5000,
            "solvers": [],
        },
        "main-cloud": {
            "files": ['data/meta.db', 'data/sc2023/results_main_detailed.csv', 'data/sc2023/results_cloud_detailed.csv'],
            "timeout": 1000,
            "solvers": [],
        },
        "main-parallel-cloud": {
            "files": ['data/meta.db', 'data/sc2023/results_main_detailed.csv', 'data/sc2023/results_parallel_detailed.csv', 'data/sc2023/results_cloud_detailed.csv'],
            "timeout": 1000,
            "solvers": [],
        },
        "special-parallel": {
            "files": ['data/meta.db', 'data/sc2023/results_special_detailed.csv', 'data/sc2023/results_parallel_detailed.csv'],
            "timeout": 5000,
            "solvers": [],
        },
        "special-cloud": {
            "files": ['data/meta.db', 'data/sc2023/results_special_detailed.csv', 'data/sc2023/results_cloud_detailed.csv'],
            "timeout": 1000,
            "solvers": [],
        },
        "special-parallel-cloud": {
            "files": ['data/meta.db', 'data/sc2023/results_special_detailed.csv', 'data/sc2023/results_parallel_detailed.csv', 'data/sc2023/results_cloud_detailed.csv'],
            "timeout": 1000,
            "solvers": [],
        },
    }

    for track, data in tracks.items():
        solvers = data["solvers"]
        if not len(solvers):
            solvers = [ GBD([file]).get_features() for file in data["files"][1:] ]
            solvers = list(itertools.chain.from_iterable(solvers)) 
            for trash in ["aresult", "vresult"]:
                if trash in solvers:
                    solvers.remove(trash)
        gen = Generator("track = main_2023", data["files"], solvers, "gen/sc2023/{}".format(track), data['timeout'])
        gen.generate_cdf_plot()
        gen.generate_portfolios_table()
        portfolio = gen.get_best_portfolio()
        gen.generate_family_wise_score_table(portfolio, "portfolio-{}".format(len(portfolio)), vbs_from=portfolio)
        
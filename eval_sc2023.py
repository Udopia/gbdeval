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

from gbd_core.api import GBD
from gbd_eval import scatter, cactus, retrieve, scores, tables, portfolio

### Solver Names:
#[ "AMSAT_", "CaDiCaL_vivinst", "Cadical_ESA", "Cadical_rel_1_5_3_Scavel", "Kissat_Inc_ESA", 
# "Kissat_MAB_Binary", "Kissat_MAB_Conflict", "Kissat_MAB_Conflict_", "Kissat_MAB_DeepWalk_", "Kissat_MAB_ESA", "Kissat_MAB_Rephases", 
# "Kissat_MAB_prop", "Kissat_MAB_prop_no_sym", "Kissat_MAB_prop_pr_no_sym", 
# "MapleCaDiCaL_LBD_990_275", "MapleCaDiCaL_LBD_990_500", "MapleCaDiCaL_PPD_500_500", "MapleCaDiCaL_PPD_950_950", 
# "MergeSat_bve_gates", "MergeSat_bve_semgates", "MergeSat_thread1", 
# "BreakID_kissat_low_sh", "MiniSat_XorEngine", 
# "PReLearn_kissat_PReLearn_kissat_sh", "PReLearn_kissat_PReLearn_tern_kissat_sh", 
# "ReEncode_kissat_ReEncode_pair_kissat_sh", 
# "SBVA_sbva_cadical", "SBVA_sbva_kissat", 
# "SeqFROST", "SeqFROST_ERE_All", "SeqFROST_NoExtend", 
# "hKis_psids", "hKis_sat_psids", "hKis_unsat", "hKissatInc_unsat", "kissat_incsp",
# "kissat_3_1_0", "tabularasat_1_0_0", "IsaSAT", 
# "kissat_hywalk_exp", "kissat_hywalk_exp_gb", "kissat_hywalk_gb" ]
###

def generate_cdf_and_cactus_plots(gbd: GBD, solvers: list[str]):
    df = retrieve.retrieve_penalized_augmented_runtimes(gbd, solvers, ["family"], "track = main_2023", max_runtime=5000, min_group_size=5)
    vbs = retrieve.retrieve_virtual_best_solver(gbd, solvers, "track = main_2023")
    df = df.merge(vbs, on='hash', how='left')
    cactus.cactus(df.copy(), solvers + ["vbs"], holy=False, to_latex="gen/sc2023/cdf.pdf")
    cactus.cactus(df.copy(), solvers + ["vbs"], holy=True, to_latex="gen/sc2023/cactus.pdf")

def generate_scatter_plot(gbd: GBD, solver0: str, solver1: str, name: str):
    df = retrieve.retrieve_penalized_augmented_runtimes(gbd, [ solver0, solver1 ], ["family"], "track = main_2023", max_runtime=5000, min_group_size=5)
    scatter.scatter(df, solver0, solver1, "family", logscale=False, to_latex="gen/sc2023/{}.pdf".format(name))
    scatter.scatter(df, solver0, solver1, "family", logscale=True, to_latex="gen/sc2023/{}_logscale.pdf".format(name))

def generate_family_wise_score_tables(gbd: GBD, solvers: list[str], name: str, vbs_from: list[str] = None):
    df = retrieve.retrieve_penalized_augmented_runtimes(gbd, solvers, ["family"], "track = main_2023", max_runtime=5000, min_group_size=5)
    all = vbs_from or solvers
    vbs = retrieve.retrieve_virtual_best_solver(gbd, all, "track = main_2023")
    df = df.merge(vbs, on='hash', how='left')
    tab = scores.scores_group_wise(df, solvers, ["family"], sortby="diff")
    tables.table(tab, solvers + [ "vbs" ], ["family"], "gen/sc2023/{}.tex".format(name), bold_min_of=solvers, min_diff=200)
    
def generate_cdf_per_family(gbd: GBD, solvers: list[str]):
    df = retrieve.retrieve_penalized_augmented_runtimes(gbd, solvers, ["family"], "track = main_2023", max_runtime=5000, min_group_size=5)
    #for fam in ["argumentation"]: 
    for fam in df["family"].unique():
        subdf = df.query("family == '{}'".format(fam))
        cactus.cdf(subdf, solvers, title=fam, num=7, 
                    #legend_separate="gen/sc2023/cdfs/leg-{}.pdf".format(fam), 
                    to_latex="gen/sc2023/cdfs/cdf-{}.pdf".format(fam))
        
def generate_portfolio_scores(gbd: GBD, solvers: list[str]):
    df = retrieve.retrieve_penalized_augmented_runtimes(gbd, solvers, [], "track=main_2023", max_runtime=5000)
    pfs = portfolio.generate_portfolios(df, solvers, max_k=4)
    tables.portfolios(pfs, "gen/sc2023/portfolios.tex")


def generate():
    csv = 'data/sc2023/results_main_detailed.csv'
    csv = 'data/sc2023/results_special_detailed.csv'
    dbs = [ 'data/meta.db', csv ]
    with GBD(dbs) as gbd:
        solvers = gbd.get_features(gbd.get_database_name(csv))
        generate_cdf_and_cactus_plots(gbd, solvers)
        #generate_cdf_per_family(gbd, solvers)
        generate_portfolio_scores(gbd, solvers)

        pairs_to_compare = {
            "sbva_cadical_kissat": [ "SBVA_sbva_cadical", "SBVA_sbva_kissat" ],
            # "sbva_cadical_breakid": [ "SBVA_sbva_cadical", "BreakID_kissat_low_sh" ],
            # "Cadical_vivinst_Kissat_310": [ "CaDiCaL_vivinst", "kissat_3_1_0" ],
        }

        for name, pair in pairs_to_compare.items():
            generate_scatter_plot(gbd, pair[0], pair[1], name)
            generate_family_wise_score_tables(gbd, pair, name, vbs_from=solvers)

        df = retrieve.retrieve_penalized_augmented_runtimes(gbd, solvers, [], "track=main_2023", max_runtime=5000)
        pfs = portfolio.generate_portfolios2(df, solvers, max_k=5, n_best=1)
        b3pf = pfs.query("k == 3")["portfolio"].values[0].split(",")
        generate_family_wise_score_tables(gbd, b3pf, "portfolio-3", vbs_from=solvers)
        
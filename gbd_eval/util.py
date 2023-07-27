import sys

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
sc2023dict = {
    "AMSAT_": "AMSAT",
    "CaDiCaL_vivinst": "CaDiCaL-vivinst",
    "Cadical_ESA": "CaDiCaL-ESA",
    "Cadical_rel_1_5_3_Scavel": "CaDiCaL-Scavel",
    "Kissat_Inc_ESA": "KissatInc-ESA",
    "Kissat_MAB_Binary": "KissatMAB-Binary",
    "Kissat_MAB_Conflict": "KissatMAB-Conflict",
    "Kissat_MAB_Conflict_": "KissatMAB-Conflict",
    "Kissat_MAB_DeepWalk_": "KissatMAB-DeepWalk",
    "Kissat_MAB_ESA": "KissatMAB-ESA",
    "Kissat_MAB_Rephases": "KissatMAB-Rephases",
    "Kissat_MAB_prop": "KissatMABprop",
    "Kissat_MAB_prop_no_sym": "KissatMABprop-nosym",
    "Kissat_MAB_prop_pr_no_sym": "KissatMABprop-pr-nosym",
    "MapleCaDiCaL_LBD_990_275": "MapleCaDiCaL-LBD-990-275",
    "MapleCaDiCaL_LBD_990_500": "MapleCaDiCaL-LBD-990-500",
    "MapleCaDiCaL_PPD_500_500": "MapleCaDiCaL-PPD-500-500",
    "MapleCaDiCaL_PPD_950_950": "MapleCaDiCaL-PPD-950-950",
    "MergeSat_bve_gates": "MergeSatBVE-gates",
    "MergeSat_bve_semgates": "MergeSatBVE-semgates",
    "MergeSat_thread1": "MergeSat",
    "BreakID_kissat_low_sh": "BreakID-Kissat",
    "MiniSat_XorEngine": "MiniSat-XorEngine",
    "PReLearn_kissat_PReLearn_kissat_sh": "PReLearn-Kissat",
    "PReLearn_kissat_PReLearn_tern_kissat_sh": "PReLearn-Kissat-tern",
    "ReEncode_kissat_ReEncode_pair_kissat_sh": "ReEncode-Kissat-pair",
    "SBVA_sbva_cadical": "SBVA-CaDiCaL",
    "SBVA_sbva_kissat": "SBVA-Kissat",
    "SeqFROST": "SeqFROST",
    "SeqFROST_ERE_All": "SeqFROST-ERE-All",
    "SeqFROST_NoExtend": "SeqFROST-NoExtend",
    "hKis_psids": "hKis-psids",
    "hKis_sat_psids": "hKis-sat-psids",
    "hKis_unsat": "hKis-unsat",
    "hKissatInc_unsat": "hKissatInc-unsat",
    "kissat_incsp": "Kissat-incsp",
    "kissat_3_1_0": "Kissat-3.1.0",
    "tabularasat_1_0_0": "TabularasaSAT",
    "IsaSAT": "IsaSAT",
    "kissat_hywalk_exp": "Kissat-hywalk-exp",
    "kissat_hywalk_exp_gb": "Kissat-hywalk-exp-gb",
    "kissat_hywalk_gb": "Kissat-hywalk-gb",
}



def name(name: str):
    dict = sc2023dict
    if name in dict:
        return dict[name]
    else:
        return name

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

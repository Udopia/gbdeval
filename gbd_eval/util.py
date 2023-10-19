import sys

sc2023dict = {
    "vbs": "VBS",
    "count": "\#",
    # Solvers in Main Track:
    "AMSAT_": "AMSAT",
    "CaDiCaL_vivinst": "Cadical vivinst",
    "Cadical_ESA": "Cadical ESA",
    "Cadical_rel_1_5_3_Scavel": "Cadical Scavel",
    "Kissat_Inc_ESA": "KissatInc-ESA",
    "Kissat_MAB_Binary": "KissatMab-Binary",
    "Kissat_MAB_Conflict": "KissatMab-Conflict",
    "Kissat_MAB_Conflict_": "KissatMab-Conflict",
    "Kissat_MAB_DeepWalk_": "KissatMab-DeepWalk",
    "Kissat_MAB_ESA": "KissatMab-ESA",
    "Kissat_MAB_Rephases": "KissatMab-Rephases",
    "Kissat_MAB_prop": "KissatMabProp",
    "Kissat_MAB_prop_no_sym": "KissatMabProp Nosym",
    "Kissat_MAB_prop_pr_no_sym": "KissatMabProp PrNosym",
    "MapleCaDiCaL_LBD_990_275": "MapleCadical LBD-990-275",
    "MapleCaDiCaL_LBD_990_500": "MapleCadical LBD-990-500",
    "MapleCaDiCaL_PPD_500_500": "MapleCadical PPD-500-500",
    "MapleCaDiCaL_PPD_950_950": "MapleCadical PPD-950-950",
    "MergeSat_bve_gates": "MergeSatBVE-gates",
    "MergeSat_bve_semgates": "MergeSatBVE-semgates",
    "MergeSat_thread1": "MergeSat",
    "BreakID_kissat_low_sh": "BreakId Kissat",
    "MiniSat_XorEngine": "MinisatXor",
    "PReLearn_kissat_PReLearn_kissat_sh": "PReLearn-Kissat",
    "PReLearn_kissat_PReLearn_tern_kissat_sh": "PReLearn-Kissat-tern",
    "ReEncode_kissat_ReEncode_pair_kissat_sh": "ReEncode-Kissat-pair",
    "SBVA_sbva_cadical": "SBVA Cadical",
    "SBVA_sbva_kissat": "SBVA Kissat",
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
    # Solvers in Cloud Track:
    "satcomp_mallob": "Mallob1600",
    "satcomp_prs_distributed": "PRS~Dist",
    "satcomp_solimul_cloud": "Mallob1600 (solimul)",
    # Solvers in Parallel Track:
    "dps_satcomp2023": "DPS",
    "nps_satcomp2023": "NPS", 
    "gimsatul": "Gimsatul", 
    "Mallob23_parallel_1": "Mallob32", 
    "mallob23_parallel_2": "Mallob64", 
    "pahkis23": "PahKis", 
    "pakisinc23": "PahKis inc", 
    "satcomp_mergesat": "Mergesat", 
    "satcomp_nopre_prs": "PRS nopre", 
    "satcomp_pkisds": "pKisDs", 
    "satcomp_pkisds_step": "pKisDs step",
    "satcomp_pkissat": "pKissat",
    "satcomp_pkissat_str": "pKissat str",
    "satcomp_prs": "PRS",
    "satcomp_solimul_parallel": "Mallob (solimul)",
}

familydict = {
    "all": "\hline All",
    "profitable-robust-production": "Production (prp)",
    "or_randxor": "Random XOR",
    "interval-matching": "Interval Matching",
    "register-allocation": "Register Allocation",
    "set-covering": "Set Covering",
    "cryptography-ascon": "Cryptography (ascon)",
    "cryptography-simon": "Cryptography (simon)",
    "mutilated-chessboard": "Mutilated Chessboard",
    "hashtable-safety": "Hashtable Safety",
    "social-golfer": "Social Golfer",
    "pigeon-hole": "Pigeon Hole",
    "hardware-verification": "Hardware Verification",
    "school-timetabling": "School Timetabling",
    "brent-equations": "Brent Equations",
    "quasigroup-completion": "Quasigroup Completion",
    "subsumptiontest": "Subsumption Test",
    "grs-fp-comm": "GRS FP Comm",
}

def name(name: str):
    if name in sc2023dict:
        return sc2023dict[name]
    elif name in familydict:
        return familydict[name]
    elif isinstance(name, str):
        return name.replace("_", "-").title()
    else:
        return number(name)
    
def number(val):
    try:
        float(val)
        return "${:.2f}$".format(val)
    except ValueError:
        return val

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

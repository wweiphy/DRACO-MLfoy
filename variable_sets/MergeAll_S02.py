variables = {}

variables["4j_ge3t"] = [
    "CSV[2]",
    "Evt_Deta_TaggedJetsAverage",
    "Evt_Dr_JetsAverage",
    "Evt_HT_wo_MET",
    "Evt_M2_TaggedJetsAverage",
    "Evt_M2_closestTo125TaggedJets",
    "Evt_M2_closestTo91TaggedJets",
    "Evt_M2_minDrJets",
    "Evt_M2_minDrTaggedJets",
    "Evt_M3",
    "Evt_MHT",
    "Evt_MTW",
    "Evt_M_TaggedJetsAverage",
    "Evt_Pt_minDrJets",
    "Evt_Pt_minDrTaggedJets",
    "Evt_blr_transformed",
    "RecoHiggs_BJet1_Pt",
    "RecoHiggs_Chi2_log",
    "RecoTTZ_Chi2TopHad",
    "RecoTTZ_Chi2TopHad_log",
    "RecoTTZ_Chi2Total",
    "RecoTTZ_Chi2Total_log",
    "RecoTTZ_Chi2WHad",
    "RecoTTZ_Chi2WHad_log",
    "RecoTTZ_TopHad_M",
    "RecoTTZ_TopHad_W_M",
    "RecoTTZ_TopLep_W_M",
    "RecoZ_BJet1_M",
    "RecoZ_BJet2_Pt",
    "RecoZ_Chi2",
    "RecoZ_Chi2_log",
    ]


variables["5j_ge3t"] = [
    "CSV[2]",
    "CSV[3]",
    "Evt_CSV_avg",
    "Evt_CSV_dev",
    "Evt_Deta_TaggedJetsAverage",
    "Evt_Dr_JetsAverage",
    "Evt_Dr_closestTo91TaggedJets",
    "Evt_M2_TaggedJetsAverage",
    "Evt_M2_closestTo125TaggedJets",
    "Evt_M2_closestTo91TaggedJets",
    "Evt_M2_minDrTaggedJets",
    "Evt_M3_oneTagged",
    "Evt_MTW",
    "Evt_Pt_minDrTaggedJets",
    "Evt_blr_transformed",
    "RecoHiggs_Chi2",
    "RecoHiggs_Chi2_log",
    "RecoHiggs_M",
    "RecoHiggs_M_log",
    "RecoTTZ_Chi2Total_log",
    "RecoTTZ_Chi2WHad_log",
    "RecoTTZ_TopHad_M",
    "RecoTTZ_TopHad_W_M",
    "RecoTTZ_TopHad_W_Pt",
    "RecoZ_Chi2",
    "RecoZ_Chi2_log",
    ]


variables["ge6j_ge3t"] = [
    "CSV[2]",
    "CSV[3]",
    "Evt_CSV_avg",
    "Evt_CSV_dev",
    "Evt_Deta_JetsAverage",
    "Evt_Deta_TaggedJetsAverage",
    "Evt_Dr_closestTo91TaggedJets",
    "Evt_M2_TaggedJetsAverage",
    "Evt_M2_closestTo125TaggedJets",
    "Evt_M2_closestTo91TaggedJets",
    "Evt_M2_minDrTaggedJets",
    "Evt_Pt_minDrTaggedJets",
    "Evt_blr",
    "Evt_blr_transformed",
    "Jet_Pt[5]",
    "N_BTagsM",
    "RecoHiggs_Chi2_log",
    #"RecoTTH_Chi2Higgs_log",
    "RecoTTZ_Chi2Total_log",
    "RecoTTZ_Chi2Z",
    "RecoTTZ_Chi2Z_log",
    "RecoTTZ_TopHad_M",
    "RecoTTZ_TopHad_W_M",
    "RecoTTZ_Z_BJet1_Pt",
    "RecoTTZ_Z_BJet2_Pt",
    "RecoTTZ_Z_M_log",
    "RecoZ_Chi2_log",
    ]


variables["ge4j_3t"] = [
    "CSV[2]",
    "CSV[3]",
    "Evt_CSV_avg",
    "Evt_CSV_avg_tagged",
    "Evt_CSV_dev",
    "Evt_CSV_min_tagged",
    "Evt_Deta_TaggedJetsAverage",
    "Evt_HT_jets",
    "Evt_HT_wo_MET",
    "Evt_M2_TaggedJetsAverage",
    "Evt_M2_closestTo125TaggedJets",
    "Evt_M2_closestTo91TaggedJets",
    "Evt_M2_minDrTaggedJets",
    "Evt_Pt_minDrTaggedJets",
    "Evt_blr_transformed",
    "RecoHiggs_Chi2",
    "RecoHiggs_Chi2_log",
    "RecoHiggs_M",
    "RecoHiggs_M_log",
    "RecoTTZ_Chi2Total_log",
    "RecoTTZ_Dphi_topLep_topHad",
    "RecoTTZ_TopHad_M",
    "RecoTTZ_TopHad_Pt",
    "RecoTTZ_TopHad_W_Pt",
    "RecoTTZ_TopLep_Pt",
    "RecoZ_BJet1_Eta",
    "RecoZ_BJet2_Pt",
    "RecoZ_Chi2_log",
    ]


variables["ge4j_ge4t"] = [
    "CSV[1]",
    "CSV[2]",
    "CSV[3]",
    "Evt_CSV_avg_tagged",
    "Evt_Deta_TaggedJetsAverage",
    "Evt_M2_closestTo125TaggedJets",
    "Evt_M2_closestTo91TaggedJets",
    "Evt_M2_minDrTaggedJets",
    "Evt_MTW",
    "Evt_Pt_minDrTaggedJets",
    "Evt_blr_transformed",
    "Evt_h0",
    "N_LooseJets",
    "RecoHiggs_Chi2",
    "RecoHiggs_Chi2_log",
    "RecoHiggs_M_log",
    "RecoTTZ_Chi2Total_log",
    "RecoTTZ_Dphi_topLep_topHad",
    "RecoTTZ_TopLep_W_M",
    "RecoZ_BJet2_Pt",
    "RecoZ_Chi2",
    "RecoZ_Chi2_log",
    "RecoZ_M_log",
    "RecoZ_Pt",
    ]

all_variables = list(set( [v for key in variables for v in variables[key] ] ))

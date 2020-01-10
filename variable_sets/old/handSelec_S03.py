variables = {}

variables["4j_ge3t"] = [
    "CSV[2]",
    "CSV[3]",
    "Evt_CSV_avg",
    "Evt_CSV_avg_tagged",
    "Evt_CSV_dev_tagged",
    "Evt_CSV_min",
    "Evt_CSV_min_tagged",
    "Evt_Deta_JetsAverage",
    "Evt_Deta_TaggedJetsAverage",
    "Evt_Dr_minDrLepJet",
    #"Evt_E_JetsAverage",
    #"Evt_Eta_JetsAverage",
    #"Evt_JetPt_over_JetE",
    "Evt_M2_TaggedJetsAverage",
    "Evt_MHT",
    "Evt_M_TaggedJetsAverage",
    "Evt_Pt_JetsAverage",
    "Evt_Pt_minDrJets",
    "Evt_Pt_minDrTaggedJets",
    #"Evt_TaggedJetPt_over_TaggedJetE",
    #"Evt_aplanarity_tags",
    "Evt_blr_transformed",
    "Evt_h1",
    "Evt_h3",
    "Jet_Pt[0]",
    #"RecoHiggs_BJet1_M",
    #"RecoHiggs_BJet1_Pt",
    #"RecoHiggs_Chi2",
    "RecoHiggs_Chi2_log",
    "RecoHiggs_Dphi",
    #"RecoHiggs_M",
    "RecoHiggs_M_log",
    #"RecoHiggs_Pt",
    "RecoTTZ_Chi2TopHad_log",
    "RecoTTZ_Chi2Total_log",
    #"RecoTTZ_Chi2WHad",
    "RecoTTZ_Chi2WHad_log",
    #"RecoTTZ_TopHad_BJet_M",
    #"RecoTTZ_TopHad_E",
    "RecoTTZ_TopHad_M",
    #"RecoTTZ_TopHad_Pt",
    "RecoTTZ_TopHad_W_M",
    #"RecoTTZ_TopLep_Pt",
    "RecoTTZ_TopLep_W_M",
    #"RecoTTZ_cosdTheta_bLep_topHad",
    "RecoZ_BJet1_M",
    #"RecoZ_BJet1_Pt",
    #"RecoZ_BJet2_E",
    #"RecoZ_Chi2",
    "RecoZ_Chi2_log",
    "RecoZ_Pt",
    ]


variables["5j_ge3t"] = [
    "CSV[2]",
    "CSV[3]",
    "Evt_CSV_avg",
    "Evt_CSV_avg_tagged",
    "Evt_CSV_dev",
    "Evt_CSV_min",
    "Evt_Deta_JetsAverage",
    "Evt_Deta_TaggedJetsAverage",
    "Evt_Dr_JetsAverage",
    #"Evt_Dr_closestTo91TaggedJets",
    "Evt_HT",
    #"Evt_HT_jets",
    #"Evt_JetPt_over_JetE",
    "Evt_M2_JetsAverage",
    "Evt_M2_TaggedJetsAverage",
    "Evt_M2_minDrJets",
    "Evt_M2_minDrTaggedJets",
    "Evt_M3",
    "Evt_MHT",
    "Evt_M_JetsAverage",
    "Evt_M_TaggedJetsAverage",
    "Evt_M_Total",
    "Evt_Pt_JetsAverage",
    "Evt_Pt_minDrJets",
    "Evt_Pt_minDrTaggedJets",
    #"Evt_blr",
    "Evt_blr_transformed",
    "Evt_h1",
    #"Evt_h2",
    "Evt_transverse_sphericity",
    "Jet_Pt[3]",
    "Jet_Pt[4]",
    "N_BTagsL",
    #"RecoHiggs_Chi2",
    "RecoHiggs_Chi2_log",
    #"RecoHiggs_M",
    "RecoHiggs_M_log",
    #"RecoTTZ_Chi2TopLep",
    "RecoTTZ_Chi2Total_log",
    #"RecoTTZ_Chi2WHad_log",
    "RecoTTZ_TopHad_M",
    #"RecoTTZ_TopLep_BJet_Eta",
    #"RecoZ_BJet1_Pt",
    #"RecoZ_BJet2_Pt",
    #"RecoZ_Chi2",
    "RecoZ_Chi2_log",
    ]


variables["ge6j_ge3t"] = [
    #"CSV[0]",
    "CSV[2]",
    "CSV[3]",
    "CSV[4]",
    "Evt_CSV_avg",
    "Evt_CSV_avg_tagged",
    "Evt_CSV_dev",
    "Evt_CSV_min_tagged",
    "Evt_Deta_JetsAverage",
    "Evt_Deta_TaggedJetsAverage",
    "Evt_Dr_TaggedJetsAverage",
    "Evt_Dr_minDrLepTag",
    "Evt_HT_jets",
    "Evt_M2_TaggedJetsAverage",
    "Evt_M_TaggedJetsAverage",
    "Evt_M_minDrLepTag",
    "Evt_Pt_minDrTaggedJets",
    "Evt_blr",
    "Evt_blr_transformed",
    "Evt_h2",
    #"Jet_CSV[0]",
    "Jet_M[0]",
    "Jet_Pt[0]",
    "Jet_Pt[4]",
    "Jet_Pt[5]",
    "N_BTagsM",
    #"RecoHiggs_Chi2",
    "RecoHiggs_Chi2_log",
    #"RecoHiggs_M",
    "RecoHiggs_M_log",
    #"RecoTTH_Chi2Higgs",
    "RecoTTH_Chi2Higgs_log",
    "RecoTTH_Higgs_M_log",
    #"RecoTTH_Higgs_Pt",
    "RecoTTZ_Chi2Total_log",
    "RecoTTZ_Chi2WHad_log",
    #"RecoTTZ_Chi2Z",
    "RecoTTZ_Chi2Z_log",
    #"RecoTTZ_TopLep_Pt",
    #"RecoTTZ_TopLep_W_M",
    #"RecoTTZ_Z_BJet2_Pt",
    #"RecoTTZ_Z_M",
    "RecoTTZ_Z_M_log",
    #"RecoZ_Chi2",
    "RecoZ_Chi2_log",
    "RecoZ_M_log",
    ]

all_variables = list(set( [v for key in variables for v in variables[key] ] ))

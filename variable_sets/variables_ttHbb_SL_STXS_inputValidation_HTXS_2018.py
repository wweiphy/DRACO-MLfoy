variables = {}

variables["ge4j_ge4t"] = [
    "Reco_ttH_hdau_pt1",
    "Reco_ttH_h_pt",
    "Reco_tHq_h_m",
    "Evt_HT_tags",
    "Reco_JABDT_tHq_log_top_m",
    "Reco_tHq_h_pt",
    "Reco_ttH_hdau_pt2",
    "Reco_tHW_h_pt",
    "Evt_Pt_TaggedJetsAverage",
    "Reco_JABDT_ttH_tophad_pt__P__toplep_pt__P__h_pt__DIV__Evt_HT__P__Evt_Pt_MET__P__Lep_Pt",
    "Evt_Dr_TaggedJetsAverage",
    "Reco_ttH_h_m",
    "Reco_ttH_bestJABDToutput",
    "Reco_JABDT_tHW_log_h_pt",
    "Reco_JABDT_tHW_log_h_m",
    "Reco_tHq_bestJABDToutput",
    "Evt_Pt_JetsAverage",
    "Reco_JABDT_tHq_log_min_hdau1_pt_hdau2_pt",
    "Reco_JABDT_ttH_log_toplep_m",
    "Evt_E_TaggedJetsAverage",
    "Reco_tHW_h_m",
    "Evt_M_TaggedJetsAverage",
    "TaggedJet_Pt[0]",
    "Reco_tHW_h_dr",
    "Reco_JABDT_tHq_log_h_pt",
    "Evt_Deta_TaggedJetsAverage",
    "Reco_tHq_h_dr",
    "Evt_Pt_minDrTaggedJets",
    "Reco_ttH_h_dr",
    "Reco_JABDT_ttH_log_h_pt",
    "Evt_M2_JetsAverage",
    ]


variables["ge4j_3t"] = [
    "Reco_JABDT_ttH_Jet_CSV_hdau1",
    "Reco_ttH_h_pt",
    "Reco_tHq_hdau_pt2",
    "Reco_tHq_hdau_pt1",
    "Evt_HT_tags",
    "Reco_JABDT_tHq_log_h_m",
    "Reco_tHq_h_pt",
    "Reco_tHW_h_pt",
    "Evt_Pt_TaggedJetsAverage",
    "Reco_JABDT_tHW_log_top_m",
    "Evt_Dr_TaggedJetsAverage",
    "Reco_WLep_Pt",
    "Evt_HT",
    "Reco_ttH_bestJABDToutput",
    "Reco_JABDT_tHW_log_h_pt",
    "Reco_JABDT_tHW_log_h_m",
    "Evt_Pt_JetsAverage",
    "Reco_JABDT_tHq_log_min_hdau1_pt_hdau2_pt",
    "Reco_tHW_bestJABDToutput",
    "Reco_tHW_h_m",
    "Evt_M_TaggedJetsAverage",
    "TaggedJet_Pt[0]",
    "Reco_tHW_h_dr",
    "Reco_JABDT_tHq_log_h_pt",
    "Evt_HT_jets",
    "Reco_tHq_h_dr",
    "Reco_ttH_h_dr",
    "Reco_JABDT_ttH_log_h_pt",
    "Reco_LeptonicW_Pt",
    "Reco_JABDT_ttH_log_h_m",
    ]

all_variables = list(set( [v for key in variables for v in variables[key] ] ))
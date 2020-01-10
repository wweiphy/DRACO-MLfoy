variables = {}

variables["ge4j_ge4t"] = [
    "Jet_Pt[2]",
    "Evt_Dr_minDrJets",
    "Evt_M3_oneTagged",
    "Evt_MHT",
    "Jet_Charge[1]",
    "Evt_Dr_minDrLepTag",
    "Evt_JetPt_over_JetE",
    "Evt_M_minDrLepTag",
    "Jet_CSV[1]",
    "CSV[1]",
    "Evt_h2",
    "Jet_M[1]",
    "Jet_Flav[1]",
    "Jet_Pt[3]",
    "CSV[0]",
    "Evt_Pt_minDrJets",
    "Jet_Flav[0]",
    "Evt_Dr_JetsAverage",
    "Evt_M_TaggedJetsAverage",
    "Evt_Dr_maxDrJets",
    "Evt_Pt_minDrTaggedJets",
    "Evt_Deta_JetsAverage",
    "Evt_M2_TaggedJetsAverage",
    "Evt_MTW",
    "Evt_M2_closestTo91TaggedJets",
    "Evt_Dr_TaggedJetsAverage",
    "Evt_Deta_TaggedJetsAverage",
    "Evt_Dr_minDrTaggedJets",
    "Evt_M2_minDrTaggedJets",
    "Evt_M2_closestTo125TaggedJets",
    ]


variables["ge4j_3t"] = [
    "Jet_Phi[2]",
    "Evt_h2",
    "Evt_CSV_avg",
    "Evt_h3",
    "Evt_JetPt_over_JetE",
    "Evt_M_TaggedJetsAverage",
    "CSV[3]",
    "Evt_Dr_maxDrTaggedJets",
    "Jet_Pt[3]",
    "Jet_Flav[3]",
    "Evt_M_Total",
    "Evt_Dr_minDrLepTag",
    "Evt_Dr_JetsAverage",
    "Evt_Pt_minDrTaggedJets",
    "Jet_CSV[0]",
    "Jet_Flav[0]",
    "Jet_CSV[1]",
    "Evt_M2_TaggedJetsAverage",
    "Evt_M2_closestTo91TaggedJets",
    "Jet_CSV[3]",
    "Jet_CSV[2]",
    "Evt_h1",
    "Evt_E_JetsAverage",
    "Evt_MTW",
    "Evt_Deta_JetsAverage",
    "Evt_Dr_TaggedJetsAverage",
    "Evt_Dr_minDrTaggedJets",
    "Evt_M2_closestTo125TaggedJets",
    "Evt_M2_minDrTaggedJets",
    "Evt_Deta_TaggedJetsAverage",
    ]

all_variables = list(set( [v for key in variables for v in variables[key] ] ))

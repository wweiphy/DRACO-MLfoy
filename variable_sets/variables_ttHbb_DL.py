variables = {}

variables["3j_2t"] = [
     "btagDiscriminatorAverage_untagged",
     ##"N_btags_Loose",
     "ptSum_jets_leptons",
     "pT_jet_tag_min_deltaR",
     "pT_jet_jet_min_deltaR",
     #"pT_tag_tag_min_deltaR",
     #"maxDeltaEta_jet_jet",
     "HT_jets",
     ##"avgDeltaR_jet_tag",
     ##"avgDeltaR_jet_jet",
     ##"jet1_pt",
     "R1_jet",
     "R1_tag",
     ##"HT_tags",
     ##"H1_tag",
     "H1_jet",
     "jet2_pt",
     #"lepton1_pt",
     "maxDeltaEta_tag_tag",
     ##"avgDeltaR_tag_tag",
     ##"minDeltaR_tag_tag",
     ##"dilepton_pt" ,
     #"minDeltaR_jet_jet",
     ##"met_pt",
     ##"bjet1_pt",
     "bjet2_pt",
     "mass_jet_tag_min_deltaR" ,
     "mass_jet_jet_min_deltaR",
     #"twist_jet_tag_max_mass",
     #"twist_jet_jet_max_mass"
    ]

variables["3j_3t"] = [
    "btagDiscriminatorAverage_tagged",
    "bjet3_btag",
    "maxDeltaEta_tag_tag",
    "maxDeltaEta_jet_jet" ,
    ##"N_btags_Tight",
    ##"jet3_btag",
    "jet3_pt",
    "avgDeltaR_tag_tag",
    "avgDeltaR_jet_tag",
    "avgDeltaR_jet_jet",
    "pT_jet_tag_min_deltaR",
    "pT_jet_jet_min_deltaR",
    "pT_tag_tag_min_deltaR",
    #"bjet2_btag",
    "bjet3_pt",
    "HT_tags",
    "HT_jets",
    "ptSum_jets_leptons",
    "jet2_pt",
    "jet1_pt",
    "minDeltaR_jet_jet",
    "minDeltaR_tag_tag",
    ##"centrality_tags",
    "mass_tag_tag_min_deltaR",
    "mass_jet_tag_min_deltaR",
    "mass_jet_jet_min_deltaR",
    "multiplicity_higgsLikeDijet15",
    ##"twist_tag_tag_max_mass",
    ##"twist_jet_tag_max_mass",
    ##"twist_jet_jet_max_mass"
    ]

variables["ge4j_2t"] = [
    ##"N_btags_Loose",
    #"btagDiscriminatorAverage_untagged" ,
   "ptSum_jets_leptons",
   "avgDeltaR_jet_tag" ,
   "HT_jets",
   "pT_jet_tag_min_deltaR" ,
    ##"pT_tag_tag_min_deltaR",
    #"avgDeltaR_jet_jet" ,
    #"pT_jet_jet_min_deltaR" ,
   "maxDeltaEta_tag_tag",
   "maxDeltaEta_jet_jet"  ,
    ##"jet2_pt",
   "R1_tag" ,
   "avgDeltaR_tag_tag" ,
   "minDeltaR_tag_tag",
    #"jet1_pt",
   "H1_tag",
    #"lepton1_pt" ,
    #"HT_tags",
   "H2_jet",
    ##"jet1_btag",
    ##"H0_jet" ,
   "btagDiscriminatorAverage_tagged",
    "R2_jet",
   "multiplicity_higgsLikeDijet15",
   "D_jet",
   "aplanarity_jet",
   ##"dilepton_pt",
   #"jet2_btag" ,
   "minDeltaR_jet_jet"
    ]

variables["ge4j_3t"] = [
   #"blr",
   "MEM",
   "bjet3_btag",
   "maxDeltaEta_tag_tag",
   #"N_btags_Tight",
   "avgDeltaR_tag_tag",
   "bjet2_btag",
   "avgDeltaR_jet_tag",
   "maxDeltaEta_jet_jet",
   "avgDeltaR_jet_jet",
   "centrality_tags",
   "bjet3_pt",
   "pT_tag_tag_min_deltaR",
   #"N_btags_Loose",
   "btagDiscriminatorAverage_untagged",
   "jet3_pt",
   "centrality_jets_leps",
   "D_jet",
   "HT_tags",
   "minDeltaR_tag_tag",
   "R2_jet",
   "pT_jet_tag_min_deltaR",
   "H2_jet",
   "aplanarity_jet",
   "btagDiscriminatorAverage_tagged",
   "pT_jet_jet_min_deltaR",
   "C_jet",
   #"ptSum_jets_leptons",
   "sphericity_jet",
   "jet4_pt",
   "jet3_btag"
    ]

variables["ge4j_ge4t"] = [
   'MEM',
   'maxDeltaEta_tag_tag',
   'maxDeltaEta_jet_jet',
   'avgDeltaR_tag_tag',
  # 'blr',
   'centrality_tags',
   'avgDeltaR_jet_tag',
   'avgDeltaR_jet_jet',
   'bjet3_btag',
   'mass_tag_tag_min_deltaR',
   'centrality_jets_leps',
   'D_tag',
   'aplanarity_tag',
  # 'N_btags_Tight',
   'R2_tag',
   'H2_tag',
   'pT_tag_tag_min_deltaR',
   'bjet4_btag',
   'D_jet',
   'C_tag',
   'H4_tag',
   'sphericity_tag' ,
   'R2_jet',
   'C_jet',
   'sphericity_jet',
   'R4_tag',
   'mass_jet_tag_min_deltaR',
   'aplanarity_jet',
   'bjet2_btag',
   'transSphericity_tag'
]

variables["ge4j_ge3t"] = [
    #'blr',
    'MEM',
    'bjet3_btag',
    #'N_btags_Tight',
    #'N_btags_Loose',
    #'N_btags_Medium',
    'avgDeltaR_tag_tag' ,
    'bjet2_btag',
    'maxDeltaEta_tag_tag',
    'btagDiscriminatorAverage_tagged',
    'H0_tag',
    'avgDeltaR_jet_tag',
    'maxDeltaEta_jet_jet',
    'HT_tags',
    'avgDeltaR_jet_jet',
    'H2_tag',
    'D_tag',
    'aplanarity_tag',
    'H3_tag',
    'minDeltaR_tag_tag',
    'R2_tag',
    'pT_tag_tag_min_deltaR',
    #'centrality_tags',
    'bjet3_pt',
    'jet3_pt',
    'R3_tag' ,
    'centrality_jets_leps',
    'jet3_btag',
    'H2_jet',
    'D_jet'
    ]

variables["jets"]= [

    "jet1_pt",
    "jet1_eta",
    "jet1_phi",
    "jet1_M",
    "jet1_btag",

    "jet2_pt",
    "jet2_eta",
    "jet2_phi",
    "jet2_M",
    "jet2_btag",

    "jet3_pt",
    "jet3_eta",
    "jet3_phi",
    "jet3_M",
    "jet3_btag",

    "jet4_pt",
    "jet4_eta",
    "jet4_phi",
    "jet4_M",
    "jet4_btag",

    "jet5_pt",
    "jet5_eta",
    "jet5_phi",
    "jet5_M",
    "jet5_btag",

    "jet6_pt",
    "jet6_eta",
    "jet6_phi",
    "jet6_M",
    "jet6_btag",

    "bjet1_pt",
    "bjet1_eta",
    "bjet2_pt",
    "bjet2_eta",
    "bjet3_pt",
    "bjet3_eta",
    "bjet1_btag",
    "bjet2_btag",
    "bjet3_btag",
]

variables["all"] = [
     "lepton1_pt",
     "lepton2_pt",

     "lepton1_eta",
     "lepton2_eta",

      "jet1_pt",
      "jet2_pt",
      "jet3_pt",
      "jet4_pt",
      "jet5_pt",
      "jet6_pt",
      "bjet1_pt",
      "bjet2_pt",
      "bjet3_pt",
      "bjet4_pt",

      "jet1_eta",
      "jet2_eta",
      "jet3_eta",
      "jet4_eta",
      "jet5_eta",
      "jet6_eta",
      "bjet1_eta",
      "bjet2_eta",
      "bjet3_eta",
      "bjet4_eta",

      "jet1_btag",
      "jet2_btag",
      "jet3_btag",
      "jet4_btag",
      "jet5_btag",
      "jet6_btag",
      "bjet1_btag",
      "bjet2_btag",
      "bjet3_btag",
      "bjet4_btag",

     "dilepton_pt",
     "dilepton_eta",
     "dilepton_M",

     "met_pt",
     "met_phi",


     "multiplicity_higgsLikeDijet15",

     "btagDiscriminatorAverage_tagged",
     "btagDiscriminatorAverage_untagged",

     "sphericity_jet",
     "sphericity_tag" ,

     "aplanarity_jet",
     "aplanarity_tag",


     "isotropy_jet",
     "isotropy_tag",

     "C_jet",
     "C_tag",

     "D_jet",
     "D_tag",

     "transSphericity_jet",
     "transSphericity_tag",

     "H0_jet",
     "H1_jet",
     "H2_jet",
     "H3_jet",
     "H4_jet",

     "H0_tag",
     "H1_tag",
     "H2_tag",
     "H3_tag",
     "H4_tag",

     "R1_jet",
     "R2_jet",
     "R3_jet",
     "R4_jet",

     "R1_tag",
     "R2_tag",
     "R3_tag",
     "R4_tag",

     "avgDeltaR_jet_jet",
     "avgDeltaR_jet_tag",
     "avgDeltaR_tag_tag",

     "centrality_jets_leps",
     "centrality_tags",

     "circularity_jet",
     "circularity_tag",

     "mass_higgsLikeDijet",
     "mass_higgsLikeDijet2",


     "mass_jet_jet_min_deltaR",
     "mass_jet_tag_min_deltaR",
     "mass_tag_tag_min_deltaR",
     "mass_tag_tag_max_mass",
     "mass_jet_jet_jet_max_pT",
     "mass_jet_tag_tag_max_pT",

     "maxDeltaEta_jet_jet",
     "maxDeltaEta_tag_tag",

     "median_mass_jet_jet",

     "minDeltaR_jet_jet",
     "minDeltaR_tag_tag",

     "pT_jet_jet_min_deltaR",
     "pT_jet_tag_min_deltaR",
     "pT_tag_tag_min_deltaR",

     "ptSum_jets_leptons",

     "HT_jets",
     "HT_tags",

     "twist_jet_jet_max_mass",
     "twist_jet_tag_max_mass",
     "twist_tag_tag_max_mass",
     "twist_tag_tag_min_deltaR"
]

#variables["ge4j_ge3t"] = list(set(variables["ge4j_ge4t"][:] + variables["ge4j_3t"][:]))
#variables["ge4j_ge3t"] = list(set(variables["ge4j_ge4t"][:] + variables["ge4j_3t"][:] + variables["jets"]))
#!! variables["ge4j_ge3t"] = ["jet1_pt", "jet2_pt"] #!!!!

all_variables = set( [v for key in variables for v in variables[key] ] )

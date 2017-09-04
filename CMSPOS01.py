import ROOT
from DataFormats.FWLite import Events, Handle

events = Events('file:/home/common/ShortExercises/GEM/RelValZMM_14_CMSSW_9_1_1_patch1-91X_upgrade2023_realistic_v1_D17-v1_GEN-SIM-RECO.root')

for e in events:
  print e.eventAuxiliary().run(), e.eventAuxiliary().event()

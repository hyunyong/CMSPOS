import ROOT
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()
from DataFormats.FWLite import Events, Handle
import os
import sys
from math import sqrt
ROOT.gROOT.SetBatch(1)

path_f = sys.argv[1]

out_root = ROOT.TFile("CMSPOS.root","RECREATE")
GE11RecHit = ROOT.TH2D("chamberRecHits", "recHits", 500, -25, 25,8,1,9)
GE11ClusterSize = ROOT.TH1D("clusterSize", "cluster Size", 25, 0, 25)
GE11Resol = ROOT.TH1D("GE11Reso", "resolution", 100, -5,5)
muonsLable, muons = "muons", Handle("vector<reco::Muon>")
gemRecHitsLabel, gemRecHits = "gemRecHits", Handle("edm::RangeMap<GEMDetId,edm::OwnVector<GEMRecHit,edm::ClonePolicy<GEMRecHit> >,edm::ClonePolicy<GEMRecHit> >")

events = Events(path_f)
for e in events:
  #print e.eventAuxiliary().run(), e.eventAuxiliary().event()
  e.getByLabel(muonsLable, muons)
  e.getByLabel(gemRecHitsLabel,gemRecHits) 
  if gemRecHits.isValid():
    for rh in gemRecHits.product():
      #print rh.gemId().region(), rh.gemId().station(), rh.gemId().layer(), rh.gemId().chamber(), rh.localPosition().x(), rh.gemId().roll()
      if rh.gemId().station() == 1:
        GE11RecHit.Fill(rh.localPosition().x(), rh.gemId().roll())
        GE11ClusterSize.Fill(rh.clusterSize())
  if muons.isValid():
    for mu in muons.product(): 
      for chamber in mu.matches():
        for seg in chamber.gemMatches:
          if seg.gemSegmentRef.gemDetId().station()  == 1:
            dx = chamber.x - seg.gemSegmentRef.get().localPosition().x() 
            GE11Resol.Fill(dx)
GE11Resol.Fit("gaus")
out_root.Write()
out_root.Close()


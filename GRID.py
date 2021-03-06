import ROOT, os, sys
from DataFormats.FWLite import Events, Handle

ROOT.gROOT.SetBatch(1)

inF = open('./rootFileListPU200.txt', 'r')
fileList = [x for x in inF]
xrootSite = "root://cms-xrd-global.cern.ch/" 

outROOT = ROOT.TFile("GridPU200.root","RECREATE")

GE11RecHit = ROOT.TH2D("chamberRecHits", "recHits", 500, -25, 25,8,1,9)
GE11ClusterSize = ROOT.TH1D("clusterSize", "cluster Size", 25, 0, 25)
GE11SimResol = ROOT.TH1D("GE11SimReso", "Simresolution", 100, -5,5)
GE11Resol = ROOT.TH1D("GE11Reso", "resolution", 100, -5,5)

gemRecHitsLabel, gemRecHits = "gemRecHits", Handle("edm::RangeMap<GEMDetId,edm::OwnVector<GEMRecHit,edm::ClonePolicy<GEMRecHit> >,edm::ClonePolicy<GEMRecHit> >")
simLabel, sim = ("g4SimHits", "MuonGEMHits", "SIM"), Handle("vector<PSimHit>")
muonsLable, muons = "muons", Handle("vector<reco::Muon>")

for f in fileList[:5]:
  print xrootSite+f
  events = Events(xrootSite+f)
  for e in events:
    e.getByLabel(gemRecHitsLabel,gemRecHits) 
    e.getByLabel(simLabel, sim)
    e.getByLabel(muonsLable, muons)
    if gemRecHits.isValid():
      for rh in gemRecHits.product():
        #print rh.gemId().region(), rh.gemId().station(), rh.gemId().layer(), rh.gemId().chamber(), rh.localPosition().x(), rh.gemId().roll()
        if rh.gemId().station() == 1:
          GE11RecHit.Fill(rh.localPosition().x(), rh.gemId().roll())
          GE11ClusterSize.Fill(rh.clusterSize())
          for sh in sim.product():
            if sh.detUnitId() == rh.gemId().rawId():
              simDx = sh.localPosition().x() - rh.localPosition().x()
              GE11SimResol.Fill(simDx)
            
    if muons.isValid():
      for mu in muons.product(): 
        for chamber in mu.matches():
          for seg in chamber.gemMatches:
            if seg.gemSegmentRef.gemDetId().station()  == 1:
              dx = chamber.x - seg.gemSegmentRef.get().localPosition().x() 
              GE11Resol.Fill(dx)

GE11SimResol.Fit("gaus")
GE11Resol.Fit("gaus")
    
outROOT.Write()
outROOT.Close()


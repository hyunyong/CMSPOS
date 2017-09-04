import ROOT, os, sys
from DataFormats.FWLite import Events, Handle

ROOT.gROOT.SetBatch(1)

inF = open(sys.argv[1], 'r')
fileList = [x for x in inF ]
xrootSite = "root://cms-xrd-global.cern.ch/" 

outROOT = ROOT.TFile("CMSPOS.root","RECREATE")

GE11RecHit = ROOT.TH2D("chamberRecHits", "recHits", 500, -25, 25,8,1,9)
GE11ClusterSize = ROOT.TH1D("clusterSize", "cluster Size", 25, 0, 25)

gemRecHitsLabel, gemRecHits = "gemRecHits", Handle("edm::RangeMap<GEMDetId,edm::OwnVector<GEMRecHit,edm::ClonePolicy<GEMRecHit> >,edm::ClonePolicy<GEMRecHit> >")

for f in fileList:
  print xrootSite+f
  events = Events(xrootSite+f)
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
outROOT.Write()
outROOT.Close()


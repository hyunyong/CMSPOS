# CMSPOS

https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSPhysicsObjectSchool2017GEM

```bash
scram p cmssw CMSSW_9_1_1_patch1
cd CMSSW_9_1_1_patch1/src
cmsenv

wget https://raw.githubusercontent.com/hyunyong/CMSPOS/master/CMSPOS.py

python CMSPOS.py

voms-proxy-init -voms cms

wget https://raw.githubusercontent.com/hyunyong/CMSPOS/master/GRID.py
wget https://raw.githubusercontent.com/hyunyong/CMSPOS/master/rootFileListPU200.txt

python GRID.py
```


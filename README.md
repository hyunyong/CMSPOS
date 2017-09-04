# CMSPOS

https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSPhysicsObjectSchool2017GEM

```bash
scram p cmssw CMSSW_9_1_1_patch1
cd CMSSW_9_1_1_patch1/src
cmsenv

voms-proxy-init -voms cms

wget https://raw.githubusercontent.com/hyunyong/CMSPOS/master/GRID.py

python GRID.py
```

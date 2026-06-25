#!/bin/bash

#PBS -N HaaAnaRD
#PBS -o /cms/data/juward/ana/Htoaa/CMSSW_15_0_18/src/HtoAA4bAnalyzer/FatJet/logs/HaaAnaRD.out
#PBS -e /cms/data/juward/ana/Htoaa/CMSSW_15_0_18/src/HtoAA4bAnalyzer/FatJet/logs/HaaAnaRD.err


cd /cms/data/juward/ana/Htoaa/CMSSW_15_0_18/src
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
export PYTHONNOUSERSITE=1


cd /cms/data/juward/ana/Htoaa/CMSSW_15_0_18/src/HtoAA4bAnalyzer/FatJet
python3 ./HaaAna_mod_RD.py .

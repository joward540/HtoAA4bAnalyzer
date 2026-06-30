#!/bin/bash/python3

#PBS -N HaaPlotter
#PBS -o /cms/data/juward/ana/Htoaa/CMSSW_15_0_18/src/HtoAA4bAnalyzer/FatJet/logs/HaaPlotter.out
#PBS -e /cms/data/juward/ana/Htoaa/CMSSW_15_0_18/src/HtoAA4bAnalyzer/FatJet/logs/HaaPlotter.err


cd /cms/data/juward/ana/Htoaa/CMSSW_15_0_18/src
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
export PYTHONNOUSERSITE=1


cd /cms/data/juward/ana/Htoaa/CMSSW_15_0_18/src/HtoAA4bAnalyzer/FatJet
python3 -s ./HtoAAto4b_Ana_Plotter_generic.py 

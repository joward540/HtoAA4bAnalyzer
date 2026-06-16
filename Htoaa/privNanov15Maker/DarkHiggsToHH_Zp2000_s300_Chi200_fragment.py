import FWCore.ParameterSet.Config as cms

# link to cards: https://gitlab.cern.ch/cms-gen/genproductions_cards/-/tree/master/MadGraph5_aMCatNLO/production/13p6TeV/DarkHiggs_noDHdecay
# gridpacks: /cvmfs/cms-griddata.cern.ch/phys_generator/gridpacks_tarball/pp/13p6TeV/madgraph/darkHiggs/ . Default values of coupling: g_q = 0.25, g_x = 1.0, theta = 0.01.

mzp = 2000
mhs = 300
mchi = 200
gridpackPath = f'/cvmfs/cms-griddata.cern.ch/phys_generator/gridpacks_tarball/pp/13p6TeV/madgraph/darkHiggs/DarkHiggs_noDHdecay_Zp{mzp}_s{mhs}_Chi{mchi}_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz'

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
                                     args = cms.vstring(gridpackPath),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(False)
)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

baseSLHATable="""
BLOCK MASS  # Mass Spectrum
# PDG code  mass     particle
   55       %m_Zp%   # Z'
   54       %m_hs%   # hs
   52       %m_dm#   # DM or Chi
# DECAY TABLE
#       PDG    Width
DECAY   52     0.00000000E+00     # DM decay
DECAY   54     1.00000000E-1      # dark higgs decays
    0.00000000E+00   3    22 5 -5 # dummy decay
    1.00000000E+00   2    25 25
"""
slhatable = baseSLHATable.replace('%m_Zp%','%e' % mzp)
slhatable = slhatable.replace('%m_hs%','%e' % mhs)
slhatable = slhatable.replace('%m_dm%','%e' % mchi)

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13600),
    SLHATableForPythia8 = cms.string('%s' % slhatable),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'TauDecays:externalMode = 2',
            'SLHA:allowUserOverride = on',
            'SLHA:minMassSM = 100.'
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters'
        )
    )
)

ProductionFilterSequence = cms.Sequence(generator)

import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

mchi = 400
mlsp = 1

GridpackPath = ('/cvmfs/cms.cern.ch/phys_generator/gridpacks/RunIII/13p6TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUSY_SMS/SMS-N2N3/SMS-N2N3_mN-%i_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz' % mchi)
externalLHEProducer = cms.EDProducer('ExternalLHEProducer',
                                     args = cms.vstring(GridpackPath),
                                     nEvents = cms.untracked.uint32(5000),
                                     numberOfParameters = cms.uint32(1),
                                     outputFile = cms.string('cmsgrid_final.lhe'),
                                     scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
                                     generateConcurrently = cms.untracked.bool(False)
                                     )

baseSLHATable="""
BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
   1000001     1.00000000E+05   # ~d_L
   2000001     1.00000000E+05   # ~d_R
   1000002     1.00000000E+05   # ~u_L
   2000002     1.00000000E+05   # ~u_R
   1000003     1.00000000E+05   # ~s_L
   2000003     1.00000000E+05   # ~s_R
   1000004     1.00000000E+05   # ~c_L
   2000004     1.00000000E+05   # ~c_R
   1000005     1.00000000E+05   # ~b_1
   2000005     1.00000000E+05   # ~b_2
   1000006     1.00000000E+05   # ~t_1
   2000006     1.00000000E+05   # ~t_2
   1000011     1.00000000E+05   # ~e_L
   2000011     1.00000000E+05   # ~e_R
   1000012     1.00000000E+05   # ~nu_eL
   1000013     1.00000000E+05   # ~mu_L
   2000013     1.00000000E+05   # ~mu_R
   1000014     1.00000000E+05   # ~nu_muL
   1000015     1.00000000E+05   # ~tau_1
   2000015     1.00000000E+05   # ~tau_2
   1000016     1.00000000E+05   # ~nu_tauL
   1000021     1.00000000E+05   # ~g
   1000022     %MLSP%           # ~chi_10
   1000023     %MCHI%           # ~chi_20
   1000025     %MCHI%           # ~chi_30
   1000035     1.00000000E+05   # ~chi_40
   1000024     1.00000000E+05   # ~chi_1+
   1000037     1.00000000E+05   # ~chi_2+
# DECAY TABLE
#         PDG            Width
DECAY   1000001     0.00000000E+00   # sdown_L decays
DECAY   2000001     0.00000000E+00   # sdown_R decays
DECAY   1000002     0.00000000E+00   # sup_L decays
DECAY   2000002     0.00000000E+00   # sup_R decays
DECAY   1000003     0.00000000E+00   # sstrange_L decays
DECAY   2000003     0.00000000E+00   # sstrange_R decays
DECAY   1000004     0.00000000E+00   # scharm_L decays
DECAY   2000004     0.00000000E+00   # scharm_R decays
DECAY   1000005     0.00000000E+00   # sbottom1 decays
DECAY   2000005     0.00000000E+00   # sbottom2 decays
DECAY   1000006     0.00000000E+00   # stop1 decays
DECAY   2000006     0.00000000E+00   # stop2 decays
DECAY   1000011     0.00000000E+00   # selectron_L decays
DECAY   2000011     0.00000000E+00   # selectron_R decays
DECAY   1000012     0.00000000E+00   # snu_elL decays
DECAY   1000013     0.00000000E+00   # smuon_L decays
DECAY   2000013     0.00000000E+00   # smuon_R decays
DECAY   1000014     0.00000000E+00   # snu_muL decays
DECAY   1000015     0.00000000E+00   # stau_1 decays
DECAY   2000015     0.00000000E+00   # stau_2 decays
DECAY   1000016     0.00000000E+00   # snu_tauL decays
DECAY   1000021     0.00000000E+00   # gluino decays
DECAY   1000022     0.00000000E+00   # neutralino1 decays
DECAY   1000023     1.00000000E-01   # neutralino2 decays
    0.00000000E+00   3    1000022   11   -11
    1.00000000E+00   2    1000022   23
DECAY   1000024     0.00000000E+00   # chargino1+ decays
DECAY   1000025     1.00000000E-01   # neutralino3 decays
    0.00000000E+00   3    1000022   11   -11
    1.00000000E+00   2    1000022   23
DECAY   1000035     0.00000000E+00   # neutralino4 decays
DECAY   1000037     0.00000000E+00   # chargino2+ decays
"""
slhatable = baseSLHATable.replace('%MCHI%','%e' % mchi)
slhatable = slhatable.replace('%MLSP%','%e' % mlsp)

def matchParams(mass):
  if mass < 124: return 76,0.64
  elif mass < 151: return 76, 0.6
  elif mass < 176: return 76, 0.57
  elif mass < 226: return 76, 0.54
  elif mass < 326: return 76, 0.51
  elif mass < 451: return 76, 0.48
  elif mass < 651: return 76, 0.45 
  elif mass < 751: return 76, 0.436
  elif mass < 851: return 76, 0.433
  elif mass < 951: return 76, 0.424
  elif mass < 1051: return 76, 0.421
  elif mass < 1151: return 76, 0.415
  elif mass < 1251: return 76, 0.407
  elif mass < 1351: return 76, 0.400
  elif mass < 1451: return 76, 0.394
  elif mass < 1551: return 76, 0.389
  elif mass < 1651: return 76, 0.384
  elif mass < 1751: return 76, 0.381
  elif mass < 1851: return 76, 0.379

qcut, tru_eff = matchParams(mchi)

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    SLHATableForPythia8 = cms.string('%s' % slhatable),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
          'JetMatching:setMad = off',
          'JetMatching:scheme = 1',
          'JetMatching:merge = on',
          'JetMatching:jetAlgorithm = 2',
          'JetMatching:etaJetMax = 5.',
          'JetMatching:coneRadius = 1.',
          'JetMatching:slowJetPower = 1',
          'JetMatching:qCut = %.0f' % qcut, #this is the actual merging scale
          'JetMatching:nQmatch = 5',
          'JetMatching:nJetMax = 2',
          'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
          'Check:abortIfVeto = on',
          'TauDecays:externalMode = 2',
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    'pythia8PSweightsSettings'
        )
    ),
    comEnergy = cms.double(13600),
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(1),
)

ProductionFilterSequence = cms.Sequence(generator)

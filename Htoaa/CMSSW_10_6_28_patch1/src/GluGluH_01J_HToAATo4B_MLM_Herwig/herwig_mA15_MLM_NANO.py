# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: Configuration/GenProduction/python/HIG-RunIISummer20UL18wmLHEGEN-02502-fragment.py --eventcontent RAWSIM,LHE,NANOAODGEN --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE,NANOAOD --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN,NANOGEN --geometry DB:Extended --era Run2_2018 --python_filename HIG-RunIISummer20UL18wmLHEGEN-02502_1_cfg.py --fileout file:HIG-RunIISummer20UL18wmLHEGEN-02502.root --number 100 --number_out 100 --no_exec --mc --nThreads=8
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018

process = cms.Process('NANOGEN',Run2_2018)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVEarly2018Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('PhysicsTools.NanoAOD.nanogen_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(1000),
        output = cms.untracked.int32(1000)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/GenProduction/python/HIG-RunIISummer20UL18wmLHEGEN-02502-fragment.py nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(1),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(20971520),
    fileName = cms.untracked.string('file:HIG-RunIISummer20UL18wmLHEGEN-02502.root'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

process.LHEoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('LHE'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:HIG-RunIISummer20UL18wmLHEGEN-02502_inLHE.root'),
    outputCommands = process.LHEEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

process.NANOAODGENoutput = cms.OutputModule("NanoAODOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:HIG-RunIISummer20UL18wmLHEGEN-02502_inNANOAODGEN.root'),
    outputCommands = process.NANOAODGENEventContent.outputCommands
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v4', '')

process.generator = cms.EDFilter("Herwig7GeneratorFilter",
    configFiles = cms.vstring(),
    crossSection = cms.untracked.double(-1),
    dataLocation = cms.string('${HERWIGPATH:-6}'),
    eventHandlers = cms.string('/Herwig/EventHandlers'),
    filterEfficiency = cms.untracked.double(1.0),
    generatorModule = cms.string('/Herwig/Generators/EventGenerator'),
    herwig7CH3AlphaS = cms.vstring(
        'cd /Herwig/Shower',
        'set AlphaQCD:AlphaIn 0.118',
        'cd /'
    ),
    herwig7CH3MPISettings = cms.vstring(
        'set /Herwig/Hadronization/ColourReconnector:ReconnectionProbability 0.4712',
        'set /Herwig/UnderlyingEvent/MPIHandler:pTmin0 3.04',
        'set /Herwig/UnderlyingEvent/MPIHandler:InvRadius 1.284',
        'set /Herwig/UnderlyingEvent/MPIHandler:Power 0.1362'
    ),
    herwig7CH3PDF = cms.vstring(
        'cd /Herwig/Partons',
        'create ThePEG::LHAPDF PDFSet_nnlo ThePEGLHAPDF.so',
        'set PDFSet_nnlo:PDFName NNPDF31_nnlo_as_0118.LHgrid',
        'set PDFSet_nnlo:RemnantHandler HadronRemnants',
        'set /Herwig/Particles/p+:PDF PDFSet_nnlo',
        'set /Herwig/Particles/pbar-:PDF PDFSet_nnlo',
        'set /Herwig/Partons/PPExtractor:FirstPDF  PDFSet_nnlo',
        'set /Herwig/Partons/PPExtractor:SecondPDF PDFSet_nnlo',
        'set /Herwig/Shower/ShowerHandler:PDFA PDFSet_nnlo',
        'set /Herwig/Shower/ShowerHandler:PDFB PDFSet_nnlo',
        'create ThePEG::LHAPDF PDFSet_lo ThePEGLHAPDF.so',
        'set PDFSet_lo:PDFName NNPDF31_lo_as_0130.LHgrid',
        'set PDFSet_lo:RemnantHandler HadronRemnants',
        'set /Herwig/Shower/ShowerHandler:PDFARemnant PDFSet_lo',
        'set /Herwig/Shower/ShowerHandler:PDFBRemnant PDFSet_lo',
        'set /Herwig/Partons/MPIExtractor:FirstPDF PDFSet_lo',
        'set /Herwig/Partons/MPIExtractor:SecondPDF PDFSet_lo',
        'cd /'
    ),
    herwig7StableParticlesForDetector = cms.vstring(
        'set /Herwig/Decays/DecayHandler:MaxLifeTime 10*mm',
        'set /Herwig/Decays/DecayHandler:LifeTimeOption Average'
    ),
    hw_7p1SettingsFor7p2 = cms.vstring(
        'read snippets/Tune-Q2.in',
        'set /Herwig/Hadronization/ColourReconnector:Algorithm Plain',
        'set /Herwig/UnderlyingEvent/MPIHandler:EnergyExtrapolation Power',
        'set /Herwig/MatrixElements/MEMinBias:OnlyValence 0',
        'set /Herwig/Partons/RemnantDecayer:PtDistribution 0',
        'set /Herwig/Partons/RemnantDecayer:ladderMult 0.63',
        'set /Herwig/Partons/RemnantDecayer:ladderbFactor 0.0',
        'set /Herwig/UnderlyingEvent/MPIHandler:DiffractiveRatio 0.21'
    ),
    hw_PSWeights_settings = cms.vstring(
        'cd /',
        'cd /Herwig/Shower',
        'do ShowerHandler:AddVariation RedHighAll 1.141 1.141  All',
        'do ShowerHandler:AddVariation RedLowAll 0.707 0.707 All',
        'do ShowerHandler:AddVariation DefHighAll 2 2 All',
        'do ShowerHandler:AddVariation DefLowAll 0.5 0.5 All',
        'do ShowerHandler:AddVariation ConHighAll 4 4 All',
        'do ShowerHandler:AddVariation ConLowAll 0.25 0.25 All',
        'do ShowerHandler:AddVariation RedHighHard 1.141 1.141  Hard',
        'do ShowerHandler:AddVariation RedLowHard 0.707 0.707 Hard',
        'do ShowerHandler:AddVariation DefHighHard 2 2 Hard',
        'do ShowerHandler:AddVariation DefLowHard 0.5 0.5 Hard',
        'do ShowerHandler:AddVariation ConHighHard 4 4 Hard',
        'do ShowerHandler:AddVariation ConLowHard 0.25 0.25 Hard',
        'do ShowerHandler:AddVariation RedHighSecondary 1.141 1.141  Secondary',
        'do ShowerHandler:AddVariation RedLowSecondary 0.707 0.707 Secondary',
        'do ShowerHandler:AddVariation DefHighSecondary 2 2 Secondary',
        'do ShowerHandler:AddVariation DefLowSecondary 0.5 0.5 Secondary',
        'do ShowerHandler:AddVariation ConHighSecondary 4 4 Secondary',
        'do ShowerHandler:AddVariation ConLowSecondary 0.25 0.25 Secondary',
        'set SplittingGenerator:Detuning 2.0',
        'cd /'
    ),
    hw_mg_merging_settings = cms.vstring(
        'cd /Herwig/EventHandlers',
        'library HwFxFx.so',
        'create Herwig::FxFxEventHandler LesHouchesHandler',
        'set LesHouchesHandler:PartonExtractor /Herwig/Partons/PPExtractor',
        'set LesHouchesHandler:HadronizationHandler /Herwig/Hadronization/ClusterHadHandler',
        'set LesHouchesHandler:DecayHandler /Herwig/Decays/DecayHandler',
        'set LesHouchesHandler:WeightOption VarNegWeight',
        'set /Herwig/Generators/EventGenerator:EventHandler  /Herwig/EventHandlers/LesHouchesHandler',
        'create ThePEG::Cuts /Herwig/Cuts/NoCuts',
        'cd /Herwig/EventHandlers',
        'create Herwig::FxFxFileReader FxFxLHReader',
        'insert LesHouchesHandler:FxFxReaders[0] FxFxLHReader',
        'cd /Herwig/Shower',
        'library HwFxFxHandler.so',
        'create Herwig::FxFxHandler FxFxHandler',
        'set /Herwig/Shower/FxFxHandler:SplittingGenerator /Herwig/Shower/SplittingGenerator',
        'set /Herwig/Shower/FxFxHandler:KinematicsReconstructor /Herwig/Shower/KinematicsReconstructor',
        'set /Herwig/Shower/FxFxHandler:PartnerFinder /Herwig/Shower/PartnerFinder',
        'set /Herwig/EventHandlers/LesHouchesHandler:CascadeHandler /Herwig/Shower/FxFxHandler',
        'set /Herwig/Partons/PDFSet_nnlo:PDFName NNPDF31_nnlo_as_0118',
        'set /Herwig/Partons/RemnantDecayer:AllowTop Yes',
        'set /Herwig/Partons/PDFSet_nnlo:RemnantHandler /Herwig/Partons/HadronRemnants',
        'set /Herwig/Particles/p+:PDF /Herwig/Partons/PDFSet_nnlo',
        'set /Herwig/Particles/pbar-:PDF /Herwig/Partons/PDFSet_nnlo',
        'set /Herwig/Partons/PPExtractor:FirstPDF  /Herwig/Partons/PDFSet_nnlo',
        'set /Herwig/Partons/PPExtractor:SecondPDF /Herwig/Partons/PDFSet_nnlo',
        'set /Herwig/Shower/ShowerHandler:PDFA /Herwig/Partons/PDFSet_nnlo',
        'set /Herwig/Shower/ShowerHandler:PDFB /Herwig/Partons/PDFSet_nnlo',
        'set /Herwig/EventHandlers/FxFxLHReader:FileName cmsgrid_final.lhe',
        'set /Herwig/EventHandlers/FxFxLHReader:WeightWarnings false',
        'set /Herwig/EventHandlers/FxFxLHReader:AllowedToReOpen No',
        'set /Herwig/EventHandlers/FxFxLHReader:InitPDFs 0',
        'set /Herwig/EventHandlers/FxFxLHReader:Cuts /Herwig/Cuts/NoCuts',
        'set /Herwig/EventHandlers/FxFxLHReader:MomentumTreatment RescaleEnergy',
        'set /Herwig/EventHandlers/FxFxLHReader:PDFA /Herwig/Partons/PDFSet_nnlo',
        'set /Herwig/EventHandlers/FxFxLHReader:PDFB /Herwig/Partons/PDFSet_nnlo',
        'set /Herwig/Shower/ShowerHandler:MaxPtIsMuF Yes',
        'set /Herwig/Shower/ShowerHandler:RestrictPhasespace Yes',
        'set /Herwig/Shower/PartnerFinder:PartnerMethod Random',
        'set /Herwig/Shower/PartnerFinder:ScaleChoice Partner',
        'set /Herwig/Shower/KinematicsReconstructor:InitialInitialBoostOption LongTransBoost',
        'set /Herwig/Shower/KinematicsReconstructor:ReconstructionOption General',
        'set /Herwig/Shower/KinematicsReconstructor:InitialStateReconOption Rapidity',
        'set /Herwig/Shower/ShowerHandler:SpinCorrelations Yes',
        'cd /Herwig/Shower',
        'set /Herwig/Shower/FxFxHandler:MPIHandler  /Herwig/UnderlyingEvent/MPIHandler',
        'set /Herwig/Shower/FxFxHandler:RemDecayer  /Herwig/Partons/RemnantDecayer',
        'set /Herwig/Shower/FxFxHandler:ShowerAlpha  AlphaQCD',
        'set FxFxHandler:HeavyQVeto Yes',
        'set FxFxHandler:HardProcessDetection Automatic',
        'set FxFxHandler:drjmin 0',
        'cd /Herwig/Shower',
        'set FxFxHandler:VetoIsTurnedOff VetoingIsOn',
        'set FxFxHandler:ETClus 20*GeV',
        'set FxFxHandler:RClus 1.0',
        'set FxFxHandler:EtaClusMax 10',
        'set FxFxHandler:RClusFactor 1.5'
    ),
    hw_user_settings = cms.vstring(
        'cd /Herwig/Shower',
        'set FxFxHandler:njetsmax 1',
        'set FxFxHandler:MergeMode TreeMG5',
        'cd /',
        'set /Herwig/Particles/h0:NominalMass 125.0'
    ),
    hw_user_settings_KenH = cms.vstring(
        'cd /',
        'cd /Herwig/Particles',
        'create ThePEG::ParticleData A0',
        'setup A0 36 A0 15 0.1 0.0 0.0 0 0 1 0',
        'create ThePEG::ParticleData GKK',
        'setup GKK 9000021 GKK 4000 16.66646 0.0 0.0 0 8 3 0',
        'create ThePEG::ParticleData R',
        'setup R 9000025 R 180 0.0005589063 0.0 0.0 0 0 1 0',
        'cd /'
    ),
    parameterSets = cms.vstring(
        'hw_user_settings_KenH',
        'hw_mg_merging_settings',
        'hw_7p1SettingsFor7p2',
        'herwig7CH3PDF',
        'herwig7CH3AlphaS',
        'herwig7CH3MPISettings',
        'herwig7StableParticlesForDetector',
        'hw_PSWeights_settings',
        'hw_user_settings'
    ),
    repository = cms.string('${HERWIGPATH}/HerwigDefaults.rpo'),
    run = cms.string('InterfaceMatchboxTest'),
    runModeList = cms.untracked.string('read,run')
)


process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/SUSY_GluGluH_01J_HToAATo4B_M-15/v1/SUSY_GluGluH_01J_HToAATo4B_M-15_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(1000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)


process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.lhe_step = cms.Path(process.externalLHEProducer)
process.generation_step = cms.Path(process.pgen)
process.nanoAOD_step = cms.Path(process.nanogenSequence)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)
process.LHEoutput_step = cms.EndPath(process.LHEoutput)
process.NANOAODGENoutput_step = cms.EndPath(process.NANOAODGENoutput)

# Schedule definition
process.schedule = cms.Schedule(process.lhe_step,process.generation_step,process.genfiltersummary_step,process.nanoAOD_step,process.endjob_step,process.RAWSIMoutput_step,process.LHEoutput_step,process.NANOAODGENoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(2)
process.options.numberOfStreams=cms.untracked.uint32(0)
process.options.numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(1)
# filter all path with the production filter sequence
for path in process.paths:
	if path in ['lhe_step']: continue
	getattr(process,path).insert(0, process.ProductionFilterSequence)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nanogen_cff
from PhysicsTools.NanoAOD.nanogen_cff import customizeNanoGEN

#call to customisation function customizeNanoGEN imported from PhysicsTools.NanoAOD.nanogen_cff
process = customizeNanoGEN(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

#KenH
process.RandomNumberGeneratorService.generator.initialSeed = 123456789

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

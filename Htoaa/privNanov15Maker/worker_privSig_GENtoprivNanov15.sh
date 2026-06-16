#!/bin/bash
fragFile=$2
nEvents=$3
### ./worker_privSig_GENtoprivNanov15.sh -prep fragmentFile.py 10
### ./worker_privSig_GENtoprivNanov15.sh -prod fragmentFile.py 10
### ./worker_privSig_GENtoprivNanov15.sh -nanogen fragmentFile.py 10
echo "Starting worker script...................."
if [ "$1" = "-prep" ] ; then
    echo "Prep mode."
elif [ "$1" = "-prod" ] ; then
    echo "Prod mode."
elif [ "$1" = "-nanogen" ] ; then
    echo "NanoGEN mode."
else
    echo "Usage: ./worker_privSig_GENtoprivNanov15.sh -prep fragmentFile.py 10"
    echo "       ./worker_privSig_GENtoprivNanov15.sh -prod fragmentFile.py 10"
    echo "invalid argument. Exit"
    exit 0
fi
 
source /cvmfs/cms.cern.ch/cmsset_default.sh
currDir=$(pwd)
ls

nThreads=8

#### step 1
if [ -r CMSSW_14_0_21/src ] ; then
    echo release CMSSW_14_0_21 already exists
else
    scram p CMSSW CMSSW_14_0_21
fi
cd CMSSW_14_0_21/src
eval `scram runtime -sh`

mkdir -p Configuration/GenProduction/python/
cp $currDir/$fragFile Configuration/GenProduction/python/
scram b
cd ../..
############for nanogen
if [ "$1" = "-nanogen" ] ; then
    ### for GS
    # cmsDriver.py Configuration/GenProduction/python/$fragFile --era Run3_2024 --customise Configuration/DataProcessing/Utils.addMonitoring --beamspot DBrealistic --step GEN,SIM,NANOGEN --conditions 140X_mcRun3_2024_realistic_v26 --datatier NANOAODSIM --eventcontent NANOAODSIM --python_filename step_nanogen_cfg.py --fileout file:nanoGENFile.root --number $nEvents --number_out -1 --no_exec --mc --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(5000)" --nThreads $nThreads || exit $?
    ### for wmLHE
    cmsDriver.py Configuration/GenProduction/python/$fragFile --era Run3_2024 --customise Configuration/DataProcessing/Utils.addMonitoring --beamspot DBrealistic --step LHE,GEN,NANOGEN --conditions 140X_mcRun3_2024_realistic_v26 --datatier NANOAODSIM --eventcontent NANOAODSIM --python_filename step_nanogen_cfg.py --fileout file:nanoGENFile.root --number $nEvents --number_out -1 --no_exec --mc --nThreads $nThreads || exit $?
    echo "from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper" >> step_nanogen_cfg.py
    echo "randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)" >> step_nanogen_cfg.py
    echo "randSvc.populate()" >> step_nanogen_cfg.py
    cmsRun step_nanogen_cfg.py || exit $?
    exit 0
fi
echo "..................Finished step 1. ls"
ls

##################### end nanogen
# cmsDriver command
### for GS
# cmsDriver.py Configuration/GenProduction/python/$fragFile --era Run3_2024 	 --customise Configuration/DataProcessing/Utils.addMonitoring 	 --beamspot DBrealistic 	 --step GEN,SIM 	 --geometry DB:Extended 	 --conditions 140X_mcRun3_2024_realistic_v26 	 --datatier GEN-SIM 	 --eventcontent RAWSIM 	 --python_filename step1_cfg.py 	 --fileout file:step1.root 	 --number $nEvents --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(5000)" --number_out -1 	 --no_exec 	 --mc || exit $?
### end GS
#### for wmLHE
cmsDriver.py Configuration/GenProduction/python/$fragFile --era Run3_2024 --customise Configuration/DataProcessing/Utils.addMonitoring --beamspot DBrealistic --step LHE,GEN,SIM --geometry DB:Extended --conditions 140X_mcRun3_2024_realistic_v26  --datatier GEN-SIM,LHE --eventcontent RAWSIM,LHE --python_filename step1_cfg.py --fileout file:step1.root --number $nEvents --number_out -1 --no_exec --mc --nThreads $nThreads || exit $?
### end wmLHE
echo "from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper" >> step1_cfg.py
echo "randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)" >> step1_cfg.py
echo "randSvc.populate()" >> step1_cfg.py

echo "..................Running step 1. ls"
ls
if [ "$1" = "-prod" ] ; then
    cmsRun step1_cfg.py || exit $?
fi
echo "..................Finished step 1. ls"
ls
### step 2
if [ -r CMSSW_14_0_21_patch2/src ] ; then
    echo release CMSSW_14_0_21_patch2 already exists
else
    scram p CMSSW CMSSW_14_0_21_patch2
fi
cd CMSSW_14_0_21_patch2/src
eval `scram runtime -sh`

mkdir -p Configuration
scram b
cd ../..

if [ "$1" = "-prep" ] ; then
    echo "Prep mode. Step 2"
    # cmsDriver command
    cmsDriver.py 	--era Run3_2024 	--customise Configuration/DataProcessing/Utils.addMonitoring 	--procModifiers premix_stage2 	--datamix PreMix 	--step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2024v14 	--geometry DB:Extended 	--conditions 140X_mcRun3_2024_realistic_v26 	--datatier GEN-SIM-RAW 	--eventcontent PREMIXRAW 	--python_filename step2_cfg.py 	--fileout file:step2.root 	--filein file:step1.root 	--number -1 	--number_out -1 	--pileup_input "dbs:/Neutrino_E-10_gun/RunIIISummer24PrePremix-Premixlib2024_140X_mcRun3_2024_realistic_v26-v1/PREMIX" 	--no_exec 	--mc --nThreads $nThreads || exit $?
fi
echo "..................Running step 2. ls"
ls
if [ "$1" = "-prod" ] ; then
    cmsRun step2_cfg.py || exit $?
fi

echo "..................Finished step 2. Remove step1.root. ls"
rm step1.root
ls

##### step 3
if [ -r CMSSW_14_0_21_patch2/src ] ; then
    echo release CMSSW_14_0_21_patch2 already exists
else
    scram p CMSSW CMSSW_14_0_21_patch2
fi
cd CMSSW_14_0_21_patch2/src
eval `scram runtime -sh`
scram b
cd ../..

if [ "$1" = "-prep" ] ; then
    echo "Prep mode. Step 3"
    # cmsDriver command
    cmsDriver.py  --era Run3_2024 --customise Configuration/DataProcessing/Utils.addMonitoring --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --conditions 140X_mcRun3_2024_realistic_v26 --datatier AODSIM --eventcontent AODSIM --python_filename step3_cfg.py --fileout file:step3.root --filein file:step2.root --number -1 --number_out -1 --no_exec --mc --nThreads $nThreads
fi
echo "..................Running step 3. ls"
ls
if [ "$1" = "-prod" ] ; then
    cmsRun step3_cfg.py
fi
echo "..................Finished step 3. Remove step2.root. ls"
rm step2.root
ls


##### step 4
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_15_0_13_patch2/src ] ; then
 echo release CMSSW_15_0_13_patch2 already exists
else
    scram p CMSSW CMSSW_15_0_13_patch2
fi
cd CMSSW_15_0_13_patch2/src
eval `scram runtime -sh`
scram b
cd ../..

if [ "$1" = "-prep" ] ; then
    echo "Prep mode. Step 3"
    cmsDriver.py 	--era Run3_2024 	--customise Configuration/DataProcessing/Utils.addMonitoring 	--step PAT 	--geometry DB:Extended 	--conditions 150X_mcRun3_2024_realistic_v2 	--datatier MINIAODSIM 	--eventcontent MINIAODSIM1 	--python_filename step4_cfg.py 	--fileout file:miniAODFile.root 	--filein file:step3.root --nThreads $nThreads --number -1 	--number_out -1 	--no_exec 	--mc || exit $?
fi
echo "..................Running step 4. MiniAOD. ls"
ls
if [ "$1" = "-prod" ] ; then
    cmsRun step4_cfg.py
fi
echo "..................Finished step 4. Remove step3.root. ls"
rm step3.root
ls

### step 4
cmsrel $CMSSWver
if [ -r CMSSW_15_0_10/src ] ; then
    echo release CMSSW_15_0_10 already exists
else
    scram p CMSSW CMSSW_15_0_10
fi
cd CMSSW_15_0_10/src
eval `scram runtime -sh`
tar xf ../../NanoTuples_Run3_2024_parT3.tar
scram b
cd ../..

##############
cmsDriver.py --python_filename nanoTuples_mc2024.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --datatier NANOAODSIM --fileout file:nanoAODFile.root --conditions 150X_mcRun3_2024_realistic_v2 --step NANO --scenario pp --filein file:miniAODFile.root --era Run3_2024 --mc -n -1 --no_exec
echo "..................Running step 4 NanoAOD. ls"
ls
if [ "$1" = "-prod" ] ; then
    cmsRun nanoTuples_mc2024.py
fi
echo "..................Finished step 4, Nano. ls"
ls


############
#cmsDriver.py --python_filename step3_cfg.py --era Run3_2024 --customise Configuration/DataProcessing/Utils.addMonitoring --mc --eventcontent AODSIM --datatier AODSIM --conditions 140X_mcRun3_2024_realistic_v26 --step RECO,RECOSIM --fileout file:step3.root --filein file:step2.root --no_exec --customise_commands "process.options.numberOfThreads=cms.untracked.uint32(8)\nprocess.options.numberOfStreams=cms.untracked.uint32(0)" --number -1     --number_out -1
 
    # cmsDriver.py 	--era Run3_2024 	--customise Configuration/DataProcessing/Utils.addMonitoring 	--procModifiers premix_stage2 	--datamix PreMix 	--step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2024v14 	--geometry DB:Extended 	--conditions 140X_mcRun3_2024_realistic_v26 	--datatier GEN-SIM-RAW 	--eventcontent PREMIXRAW 	--python_filename step2_cfg.py 	--fileout file:step2.root 	--filein file:step1.root 	--number -1 	--number_out -1 	--pileup_input "dbs:/Neutrino_E-10_gun/RunIIISummer24PrePremix-Premixlib2024_140X_mcRun3_2024_realistic_v26-v1/PREMIX" 	--no_exec 	--mc 	--customise_commands "process.options.numberOfThreads=cms.untracked.uint32(8)\nprocess.options.numberOfStreams=cms.untracked.uint32(0)" || exit $?

    # ## step 2 CMSSW_14 only
    # cmsDriver.py --python_filename step2_cfg.py --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 140X_mcRun3_2024_realistic_v26 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2024v14 --procModifiers premix_stage2 --nThreads 8 --datamix PreMix --era Run3_2024 --filein file:step1.root --fileout file:step2.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIIISummer24PrePremix-Premixlib2024_140X_mcRun3_2024_realistic_v26-v1/PREMIX" 	--no_exec --number -1     --number_out -1

    # ## step 3 CMSSW_14 works
    # cmsDriver.py --python_filename step3_cfg.py --mc --eventcontent AODSIM --datatier AODSIM --conditions 140X_mcRun3_2024_realistic_v26 --step RAW2DIGI,L1Reco,RECO,RECOSIM --nThreads 4 --era Run3_2024 --filein file:step2.root --fileout file:step3.root --no_exec --number -1     --number_out -1
    # cmsDriver.py --python_filename step3_cfg.py --mc --eventcontent AODSIM --datatier AODSIM --conditions 150X_mcRun3_2024_realistic_v2 --step RAW2DIGI,L1Reco,RECO,RECOSIM --nThreads 4 --era Run3_2024 --filein file:step2.root --fileout file:step3.root --no_exec --number -1     --number_out -1

    # #########
    # cmsDriver.py step1 --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 130X_mcRun3_2023_realistic_postBPix_v2 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2023v12 --procModifiers premix_stage2 --nThreads 4 --geometry DB:Extended --datamix PreMix --era Run3_2023  --filein file:step-1.root --fileout file:step0.root --pileup_input "dbs:/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer23BPix_130X_mcRun3_2023_realistic_postBPix_v1-v1/PREMIX"


    # cmsDriver.py step2 --mc --eventcontent AODSIM --datatier AODSIM --conditions 130X_mcRun3_2023_realistic_postBPix_v2 --step RAW2DIGI,L1Reco,RECO,RECOSIM --nThreads 4 --geometry DB:Extended --era Run3_2023  --fileout file:step1.root

#!/bin/sh
miniFile=$1
nanoFile=$2
eosAddr=$3
eosPath=$4
echo "At condor ................................................ OS:"
cat /etc/os-release
echo "---------------------------------------------------------------"

######### cmsconnect specific
unset PYTHONPATH
######### cmsconnect specific ends
if [[ $miniFile == /store* ]]; then
    miniFile="root://cmsxrootd.fnal.gov/${miniFile}"
    #miniFile="root://cms-xrd-global.cern.ch/${miniFile}"
    #miniFile="root://xrootd-cms.infn.it/${miniFile}"
fi

nanoExists=0
gfal-ls $outFileLoc$nanoFile
if [ $? == 0 ] ; then
    nanoExists=1
    echo "File exists at the destination."
fi

gfal-copy $miniFile miniAODFile.root
# xrdcp --retry 3 $miniFile miniAODFile.root
if [ -f miniAODFile.root ] ; then
    echo ".........copied MiniAOD file...."
else
    echo "ERROR_xrdcp_in"
    exit 10
fi
ls
#############

CMSSWver=CMSSW_15_0_10
# eosAddr="root://cmseos.fnal.gov"
# eosPath="/store/user/lpchadwxmet/Run2Run3/BG_RunIII2024Summer24NanoAODv15_v1/"
# eosPath="/store/user/lpchadwxmet/Run2Run3/Sig_NanoV9ParTV2/"
# outFileLoc="root://cmseos.fnal.gov//store/user/vhegde/Physics/DarkHiggsPrivSamples/NanoV9_with_partTV2/"
outFileLoc="${eosAddr}/${eosPath}"
###############
unset PERL5LIB # cmsconnect specific
echo "At condor node..."
pwd
currDir=$(pwd)
echo "ls........"
ls
echo "Setting up CMSSW......"
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel $CMSSWver
cd $CMSSWver/src
eval `scram runtime -sh`
if [ $nanoExists -eq 1 ]; then
    if root -l -b -q -e 'gEnv->SetValue("TFile.Recover", 0); bool is_zombie = TFile::Open("'$outFileLoc${nanoFile}'")->IsZombie(); return is_zombie ? 1 : 0'; then
	echo "FULLSUCCESS"
	echo "File exists at the destination Not  and not a zombie. Not running the job."
	rm *.root
	rm *.py
	exit 0
    fi
fi
tar xf ../../NanoTuples_Run3_2024_parT3.tar
scram b
cd ../..
echo ".............Done CMSSW...."
##############
if [[ "$miniFile" == *"/store/data/Run2024"* ]]; then
    echo "iiiiiiiiiiiiiiiiii treating the miniAOD file as data"
    echo ".........Running cmsRun nanoTuples_data2024.py"
    cmsRun nanoTuples_data2024.py
else
    echo "iiiiiiiiiiiiiiiiii treating the miniAOD file as MC"
    cmsDriver.py  --python_filename nanoTuples_mc2024.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --datatier NANOAODSIM --fileout file:nanoAODFile.root --conditions 150X_mcRun3_2024_realistic_v2 --step NANO --scenario pp --filein file:miniAODFile.root --era Run3_2024 --mc -n -1 --no_exec
    #cmsDriver.py --python_filename nanoTuples_mc2018.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --datatier NANOAODSIM --fileout file:nanoAODFile.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein file:miniAODFile.root --era Run2_2018,run2_nanoAOD_106Xv2 --mc -n -1 --no_exec

    echo "process.MessageLogger.cerr.FwkReport.reportEvery = 1000" >> nanoTuples_mc2024.py
    echo ".........Done cmsDriver. Running cmsRun nanoTuples_mc2024.py"
    cmsRun nanoTuples_mc2024.py
fi


echo "......... Done cmsRun. Copying output file"
mv nanoAODFile.root $nanoFile
rm miniAODFile.root
if root -l -b -q -e 'bool is_zombie = TFile("'${nanoFile}'").IsZombie(); return is_zombie ? 1 : 0'; then
    echo "Not a zombie root file when created."
else
    echo "ERROR: Zombie root file created. Exiting"
    rm *.root
    rm *.py
    rm *.tar
    exit 10
fi
######### cmsconnect specific; undo cmsenv to use gfal-copy
export PATH=$(echo $PATH | tr ':' '\n' | grep -v cmssw | tr '\n' ':' | sed 's/:$//')
export LD_LIBRARY_PATH=$(echo $LD_LIBRARY_PATH | tr ':' '\n' | grep -v cmssw | tr '\n' ':' | sed 's/:$//')
unset -f cmsenv
unset -f cmsrel
######### cmsconnect specific ends
function repeated_copy() {
    local nanoFile=$1
    local outFileLoc=$2
    local n=$3
    for ((i=1; i<=$n; i++))
    do
	echo "Copy trial ${i}"
	gfal-copy -f $nanoFile $outFileLoc
	if [ $? == 0 ] ; then
	    gfal-ls $outFileLoc$nanoFile
	    if [ $? == 0 ] ; then
		return 0
	    fi
	else
	    echo "gfal-copy failed. Trying xrdcp"
	    sleep 10
	    xrdcp --retry 3 -f $nanoFile $outFileLoc
	fi
	sleep 2
	gfal-ls $outFileLoc$nanoFile
	if [ $? == 0 ] ; then
	    return 0
	fi
	sleep 60
    done
    echo "All copy attempts failed."
    return 1
}

exitCode=0
if repeated_copy $nanoFile $outFileLoc 5; then
    cd $CMSSWver/src
    eval `scram runtime -sh`
    if root -l -b -q -e 'gEnv->SetValue("TFile.Recover", 0); bool is_zombie = TFile::Open("'$outFileLoc${nanoFile}'")->IsZombie(); return is_zombie ? 1 : 0'; then
	echo "Not a zombie root file after transfer to destination."
    else
	echo "ERROR: Zombie root file transferred. Exiting"
	exitCode=10
    fi
    echo "FULLSUCCESS"
else
    echo "Failed to copy n times"
    exitCode=10
fi

#########
# gfal-copy -f $nanoFile $outFileLoc
# if [ $? != 0 ] ; then
#     echo "gfal-copy failed. Trying xrdcp"
#     xrdcp --retry 3 -f $nanoFile $outFileLoc
# fi
# ls
# ##########
# echo "DONE. Checking output file's existance."
# exitCode=0
# #xrdfs $eosAddr ls --retry 3 $eosPath/$nanoFile
# gfal-ls $outFileLoc$nanoFile
# if [ $? != 0 ] ; then
#     echo "ERROR_cp_out1" >&2
#     sleep 60
#     gfal-copy -f $nanoFile $outFileLoc
#     if [ $? != 0 ] ; then
# 	echo "Tried gfal-copy after some time. No success"
# 	exitCode=1
#     fi
# else
#     echo "FULLSUCCESS"
# fi
###########
echo ".......... finished production and copying. Delete .root and .py from local area..........."
cd $currDir
rm *.root
rm *.py
rm *.tar
rm -rf $CMSSWver
exit $exitCode

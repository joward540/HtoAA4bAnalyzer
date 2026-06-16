#!/bin/sh
model=$1
jobID=$2
nEvents=$3
outFileLoc=$4

unset PERL5LIB
echo "At condor node..."
pwd
currDir=$(pwd)
echo "ls........"
ls

# cp Template_DarkHiggs-fragment.py ${model}_fragment.py

# ### assign masses
# MASS_MZP=${model##*_Zp}; MASS_MZP=${MASS_MZP%%_*}
# MASS_MHS=${model##*_s}; MASS_MHS=${MASS_MHS%%_*}
# MASS_MCHI=${model##*_Chi}

# sed -i "s|MASS_MZP|${MASS_MZP}|" ${model}_fragment.py
# sed -i "s|MASS_MHS|${MASS_MHS}|" ${model}_fragment.py
# sed -i "s|MASS_MCHI|${MASS_MCHI}|" ${model}_fragment.py
#########

echo "..........set fragment file. Gridpack used:"
grep cvmfs ${model}_fragment.py

ls
echo "..........starting production......"
./worker_privSig_GENtoprivNanov15.sh -prod ${model}_fragment.py $nEvents
if [ $? == 0 ] ; then
    echo "Finished production.........."
else
    rm *.root
    echo "ERROR. Failed production exit 1"
    exit 1
fi
ls

############ copy files
function repeated_copy() {
    local outputFile=$1
    local outFileLoc=$2
    local n=$3
    for ((i=1; i<=$n; i++))
    do
	echo "Copy trial ${i}"
	gfal-copy -f $outputFile $outFileLoc
	if [ $? == 0 ] ; then
	    gfal-ls $outFileLoc$outputFile
	    if [ $? == 0 ] ; then
		return 0
	    fi
	else
	    echo "gfal-copy failed. Trying xrdcp"
	    sleep 10
	    xrdcp --retry 3 -f $outputFile $outFileLoc
	fi
	sleep 2
	gfal-ls $outFileLoc$outputFile
	if [ $? == 0 ] ; then
	    return 0
	fi
	sleep 60
    done
    echo "All copy attempts failed."
    return 1
}

exitCode=0
mv miniAODFile.root PrivSample_${model}_RunIII2024Summer24MiniAODv6_job${jobID}.root
mv nanoAODFile.root PrivSample_${model}_custom_RunIII2024Summer24NanoAODv15_job${jobID}.root

echo "copying miniAOD......"
if repeated_copy PrivSample_${model}_RunIII2024Summer24MiniAODv6_job${jobID}.root $outFileLoc 5; then
    echo "Done copying miniAOD......"
else
    echo "Failed to copy miniAOD."
    exitCode=10
fi
echo "copying nanoAOD......"
if repeated_copy PrivSample_${model}_custom_RunIII2024Summer24NanoAODv15_job${jobID}.root $outFileLoc 5; then
    echo "Done copying nano......"
else
    echo "Failed to copy nanoaod."
    exitCode=10
fi

echo "delete files from local area...."
rm -rf CMSSW* *.root *.py *.tar
if [ "${exitCode}" -eq 10 ]; then
    echo "ERROR : Output file copy failed."
    exit $exitCode
else
    echo "FULLSUCCESS"
    exit 0
fi
# if repeated_copy $outputFile $outFileLoc 5; then
#     cd $CMSSWver/src
#     eval `scram runtime -sh`
#     if root -l -b -q -e 'gEnv->SetValue("TFile.Recover", 0); bool is_zombie = TFile::Open("'$outFileLoc${outputFile}'")->IsZombie(); return is_zombie ? 1 : 0'; then
# 	echo "Not a zombie root file after transfer to destination."
#     else
# 	echo "ERROR: Zombie root file transferred. Exiting"
# 	exitCode=10
#     fi
#     echo "FULLSUCCESS"
# else
#     echo "Failed to copy n times"
#     exitCode=10
# fi


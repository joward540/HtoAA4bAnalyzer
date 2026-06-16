#!/bin/sh
# ./submitJobs_NanoGen.sh DarkHiggsToWW_Zp2000_s200_Chi200_fragment.py 1000 50
#
fragFile=$1
model=$(echo "$fragFile" | sed 's/\_fragment.py$//')
nEventsPerJob=$2
nJobs=$3
#########
outFileDest="root://cmseos.fnal.gov//store/user/lpchadwxmet/Run2Run3/privateSamples_NanoGEN/${model}/"
gfal-mkdir -p $outFileDest || exit $?
echo "Output will go to ${outFileDest} . Files inside this directory will be overwritten if the output file names match."
#########
exeAtWorker="wraper_NanoGen.sh"
filesToTransfer="worker_privSig_GENtoprivNanov15.sh,${fragFile}"
jdl_file="condor_${model}.submit"
log_prefix="condor_${model}"

echo "universe = vanilla">$jdl_file
echo "Executable = ${exeAtWorker}">>$jdl_file
echo "Arguments = $model \$(Item) $nEventsPerJob ${outFileDest}">>$jdl_file
echo "Requirements = HAS_SINGULARITY == True">>$jdl_file
echo "+SingularityImage = \"/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el9:latest\"">>$jdl_file
echo "use_x509userproxy = true">>$jdl_file
echo "Should_Transfer_Files = YES">>$jdl_file
echo "WhenToTransferOutput = ON_EXIT_OR_EVICT">>$jdl_file
echo "RequestCpus = 8">>$jdl_file
echo "RequestMemory = 15600">>$jdl_file
echo "Transfer_Input_Files = ${filesToTransfer}">>$jdl_file
echo "Output = log/${log_prefix}_job\$(Item).stdout">>$jdl_file
echo "Error = log/${log_prefix}_job\$(Item).stderr">>$jdl_file
echo "Log = log/${log_prefix}_job\$(Item).condor">>$jdl_file
echo "notification = never">>$jdl_file
echo "success_exit_code = 0">>$jdl_file
echo "on_exit_hold = (ExitCode != 0)">>$jdl_file
echo "queue from seq 1 $nJobs |">>$jdl_file

###########
condor_submit ${jdl_file}

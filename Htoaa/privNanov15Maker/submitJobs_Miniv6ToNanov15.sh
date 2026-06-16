#!/bin/sh
# ./submitJobs_Miniv6ToNanov15.sh MiniAODv6_TTtoLNu2Q_13p6TeV_v1.txt
# 
txtFile=$1
model=$(echo "$txtFile" | sed 's/^MiniAODv6_//;s/\.txt$//')
exeAtWorker="worker_Miniv6ToNanov15.sh"
filesToTransfer="NanoTuples_Run3_2024_parT3.tar,nanoTuples_data2024.py,Cert_Collisions2024_378981_386951_Golden.json"

eosAddr="root://cmseos.fnal.gov"
eosPath="/store/user/lpchadwxmet/Run2Run3/Data_Run2024_MINIv6NANOv15_v2/${model}/"
#eosPath="/store/user/lpchadwxmet/Run2Run3/privateSamples_RunIII2024Summer24/ParTV2V3_Nanov15_v2/${model}/"
#eosPath="/store/user/lpchadwxmet/Run2Run3/BG_RunIII2024Summer24NanoAODv15_v2/${model}/"
gfal-mkdir $eosAddr"/"$eosPath || exit $?
echo "Output will go to ${eosAddr}/${eosPath}"

####
outFname="Summer24NanoAODv15_${model}_job\$(ItemIndex).root"
inFname=$line
jdl_file="condor_${model}_jobs.jdl"
log_prefix="condor_${model}_job\$(ItemIndex)"

########
echo "universe = vanilla">$jdl_file
echo "Executable = $exeAtWorker">>$jdl_file
echo "Arguments = \$(inFname) $outFname $eosAddr $eosPath">>$jdl_file
echo "use_x509userproxy = true">>$jdl_file
echo "Should_Transfer_Files = YES">>$jdl_file
echo "WhenToTransferOutput = ON_EXIT_OR_EVICT">>$jdl_file
echo "RequestCpus = 4">>$jdl_file
echo "Requirements = HAS_SINGULARITY == True">>$jdl_file
echo "+SingularityImage = \"/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el9:latest\"">>$jdl_file
echo "Transfer_Input_Files = ${filesToTransfer}">>$jdl_file
echo "Output = log/${log_prefix}.stdout">>$jdl_file
echo "Error = log/${log_prefix}.stderr">>$jdl_file
echo "Log = log/${log_prefix}.condor">>$jdl_file
echo "notification = never">>$jdl_file
############# when you know that jobs run fine, but fail because of root file I/O or site issues add these:
echo "max_retries = 5">>$jdl_file
echo "success_exit_code = 0">>$jdl_file
echo "on_exit_hold = (ExitCode != 0)">>$jdl_file
echo "periodic_hold = (JobStatus == 2) && (time() - JobCurrentStartDate) > (7 * 3600)">>$jdl_file
echo "periodic_hold_reason = \"Job ran for more than seven hours\"">>$jdl_file
echo "periodic_hold_subcode = 42">>$jdl_file
echo "periodic_release = (HoldReasonSubCode == 42) || (ExitCode == 10)">>$jdl_file
# echo "periodic_vacate = (time() - QDate) > (8 * 3600)">>$jdl_file
# echo "job_machine_attrs = Machine">>$jdl_file
# echo "job_machine_attrs_history_length = 4">>$jdl_file
# echo "requirements = HAS_SINGULARITY == True && target.machine =!= MachineAttrMachine1 && target.machine =!= MachineAttrMachine2 && target.machine =!= MachineAttrMachine3">>$jdl_file
# echo "on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)">>$jdl_file # Remove from the queue ONLY if exit code signals successful job (not a copy error)
# echo "periodic_hold = ((JobStatus == 2) && ((time() - EnteredCurrentStatus) > (24*60*60))) || (ExitCode == 10)">>$jdl_file # JobStatus==2 is 'Running'
# echo "periodic_release  = (HoldReasonCode == 3) && (NumJobStarts < 5)">>$jdl_file
# echo "on_exit_hold = (ExitCode != 0)">>$jdl_file
echo "queue inFname from $txtFile">>$jdl_file
condor_submit $jdl_file

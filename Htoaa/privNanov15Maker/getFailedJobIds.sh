#!/bin/sh
#./getFailedJobIds.sh MiniAODv6_TBbarQto2Q-t-channel-4FS_13p6TeV.txt
txtFile=$1
model=$(echo "$txtFile" | sed 's/^MiniAODv6_//;s/\.txt$//')

ids=""
for i in $(grep -L FULLSUCCESS log/condor_${model}_job*.stdout)
do
    filename=$i
    basename=$(basename "$filename" .stdout)
    i_i=${basename#*job}
    ids=${ids}","$i_i
done

######### Add these lines only when jobs are not running!!!!!!!!!!
for i in log/condor_${model}_job*.condor
do
    filename=$(echo "$i" | sed 's/\.condor$/\.stdout/')
    if [ ! -f "$filename" ]; then
	filename=$i
	basename=$(basename "$filename" .condor)
	i_i=${basename#*job}
	ids=${ids}","$i_i
    fi
done

if [ "$ids" != "" ]; then
    echo "python3 makeFailedJobResubScript.py condor_${model}_jobs.jdl MiniAODv6_${model}.txt ${ids:1}"
else
    echo "${model} is ok"
fi

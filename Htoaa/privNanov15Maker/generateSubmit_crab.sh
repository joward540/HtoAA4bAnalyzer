#!/bin/sh
inputTextFile=$1
for line in $(cat $inputTextFile)
do
    a=$line
    b="${a//\//_}"   # _JetMET0_Run2024D-MINIv6NANOv15-v1_MINIAOD
    reqName="${b#_}"       # remove first leading underscore
    echo "RequestName $reqName"
    cp template_crabConfig_file.py crabConfig_${reqName}.py
    python3 replceText.py crabConfig_${reqName}.py 'REQUEST_NAME' $reqName
    python3 replceText.py crabConfig_${reqName}.py 'DATASET_NAME' $line
    crab submit -c crabConfig_${reqName}.py >> submitLog.log
done

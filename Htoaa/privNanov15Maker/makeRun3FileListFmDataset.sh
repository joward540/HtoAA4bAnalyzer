#!/bin/bash
if [[ $1 == *".txt" && -f "$1" ]]; then
    echo "making file list for every dataset listed in ${1}"
    IFS=$'\n'  # Set Internal Field Separator to newline
    for i in "$@"
    do
        for line in $(cat $i)
	do
	    # echo $line
	    tempString=${line#/} # remove first /
	    output=$(echo "$tempString" | sed 's#/#_#') # replace / with _. It looks like ZJets*pythia8_RunII*
	    output=$(echo "$output" | sed 's#/#_#') # replace another / with _.
	    endStr=$(echo "$line" | sed 's/.*_TuneCP5//') # everything after _TuneCP5
	    output=$(echo "$output" | sed 's/_TuneCP5.*//') # everything up to _TuneCP5.
	    output=MiniAODv6_${output}_13p6TeV.txt
	    
	    echo $output
	    if [[ $endStr == *"_ext"* ]]; then
		echo "$line is an extension. Will append to $output"
		dasgoclient -query="file dataset=${line}" >> $output
	    else
		dasgoclient -query="file dataset=${line}" > $output
	    fi
	    # 
	done
    done
fi

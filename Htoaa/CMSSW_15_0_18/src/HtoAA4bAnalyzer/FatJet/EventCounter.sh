#!/usr/bin/env bash

base="/cms/data/store/user/hatake/ParTV2V3_Nanov15_v2"
pattern="Summer24NanoAODv15_*_13p6TeV_job*.root"

printf "%-55s %10s %15s\n" "Dataset" "Files" "Events"
printf "%-55s %10s %15s\n" "-------" "-----" "------"

for folder in "$base"/*/; do
    [[ -d "$folder" ]] || continue

    dataset=$(basename "$folder")

    file_count=$(
        find "$folder" -maxdepth 1 -type f -name "$pattern" |
        wc -l
    )

    if [[ "$file_count" -eq 0 ]]; then
        printf "%-55s %10d %15d\n" "$dataset" 0 0
        continue
    fi

    event_count=$(
        root -l -b -q -e "
            TChain chain(\"Events\");
            chain.Add(\"${folder}${pattern}\");
            std::cout << \"EVENT_COUNT=\" << chain.GetEntries()
                      << std::endl;
        " 2>/dev/null |
        awk -F= '/EVENT_COUNT=/{print $2}'
    )

    printf "%-55s %10d %15d\n" \
        "$dataset" "$file_count" "$event_count"
done

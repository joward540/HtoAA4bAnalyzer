# python3 makeFailedJobResubScript.py condor_Zto2Nu-2Jets_Bin-1J-PTNuNu-100to200_13p6TeV_jobs.jdl MiniAODv6_Zto2Nu-2Jets_Bin-1J-PTNuNu-100to200_13p6TeV.txt 0,5
import sys

if len(sys.argv) != 4:
    print("Usage: python3 makeFailedJobResubScript.py condor_PROCESS_jobs.jdl MiniAODv6_PROCESS.txt IDS_COMMA_SEPARATED")
    exit()
    
subFile = sys.argv[1]
txtFile = sys.argv[2]
jobIdsAll = sys.argv[3].split(',')

f_txt = open(txtFile, 'r')
f_txt_cont = f_txt.readlines()

jobIds = list(dict.fromkeys(jobIdsAll)) # non-repeated
for j in jobIds:
    f_toRunOn = f_txt_cont[int(j)].rstrip()
    #    print(f_toRunOn)
    sub_file_name = subFile.replace("jobs", f"job{j}")
    sub_file = open(sub_file_name, "w")
    with open(subFile, "r") as f_subMain:
        for line in subFile:
            line = f_subMain.readline()
            if "$(inFname)" in line:
                line = line.replace("$(inFname)", f_toRunOn)
            if "$(ItemIndex)" in line:
                line = line.replace("$(ItemIndex)", j)
            if line.upper().startswith("QUEUE"):
                line = "queue 1"
                
            sub_file.write(line)
    sub_file.close()
    print(f"condor_submit {sub_file_name}")
f_txt.close()

from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'JetMET1_Run2024I-MINIv6NANOv15-v1_MINIAOD'
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'CMSSW_15_0_10/src/PhysicsTools/NanoTuples/python/nanoTuples_data2024.py'

config.General.transferLogs = True
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 480

config.Data.inputDataset = '/JetMET1/Run2024I-MINIv6NANOv15-v1/MINIAOD'
config.Data.lumiMask = 'Cert_Collisions2024_378981_386951_Golden.json'
#config.Data.runRange = '380625-380625'
#config.Data.splitting = 'LumiBased'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False

# This string is used to construct the output dataset name
config.Data.outputDatasetTag = config.General.requestName
# Where the output files will be transmitted to
config.Site.storageSite = 'T3_US_FNALLPC'
config.Data.outLFNDirBase  = '/store/group/lpchadwxmet/Run2Run3/Data_Run2024_MINIv6NANOv15_v1/'

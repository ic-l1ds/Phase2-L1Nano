
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'hh4b'
config.General.workArea = 'hh4b'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'L1nano_wjets.py'
config.JobType.maxMemoryMB = 2500
# config.JobType.numCores = 8

config.Data.inputDataset = '/GluGluToHHTo4B_node_SM_TuneCP5_14TeV-amcatnlo-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_AllTP_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#NJOBS = 100
#config.Data.totalUnits = config.Data.unitsPerJob * NJOBS

config.Data.outLFNDirBase = '/store/user/jleonhol/samples/l1scouting/Phase2/'
config.Data.publication = True
config.Data.outputDatasetTag = 'Phase2L1Nano'

config.Site.storageSite = 'T2_UK_London_IC'

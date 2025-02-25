import os

crab = """

from CRABClient.UserUtilities import config
config = config()

config.General.requestName = '{name}'
config.General.workArea = '{name}'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'L1nano_wjets.py'
config.JobType.maxMemoryMB = 2500
# config.JobType.numCores = 8

config.Data.inputDataset = '{d}'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#NJOBS = 100
#config.Data.totalUnits = config.Data.unitsPerJob * NJOBS

config.Data.outLFNDirBase = '/store/user/jleonhol/samples/l1scouting/Phase2/'
config.Data.publication = True
config.Data.outputDatasetTag = 'Phase2L1Nano'

config.Site.storageSite = 'T2_UK_London_IC'


"""

samples = {
    "QCD_Pt-20To30": "/QCD_Pt-20To30_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
    "QCD_Pt-30To50": "/QCD_Pt-30To50_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
    "QCD_Pt-50To80": "/QCD_Pt-50To80_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
    "QCD_Pt-80To120": "/QCD_Pt-80To120_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
    "QCD_Pt-120To170": "/QCD_Pt-120To170_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
    "QCD_Pt-170To300": "/QCD_Pt-170To300_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
    "QCD_Pt-300To470": "/QCD_Pt-300To470_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
    "QCD_Pt-470To600": "/QCD_Pt-470To600_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
    "QCD_Pt-600ToInf": "/QCD_Pt-600ToInf_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
    "bbtt": "/GluGluToHHTo2B2Tau_node_SM_TuneCP5_14TeV-madgraph-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_AllTP_140X_mcRun4_realistic_v4-v2/GEN-SIM-DIGI-RAW-MINIAOD"
}

for name, d in samples.items():
    if os.path.exists(name):
        continue
    with open(f"crab_submit_{name}.py", "w+") as f:
        f.write(crab.format(name=name, d=d))

    os.system(f"crab submit crab_submit_{name}.py")

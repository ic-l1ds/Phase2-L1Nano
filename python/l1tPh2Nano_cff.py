import FWCore.ParameterSet.Config as cms
# from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.common_cff import *

l1tPh2NanoTask = cms.Task()

### P2GT objects
from PhysicsTools.L1Nano.l1tPh2GTtables_cff import *
def addPh2GTObjects(process):
    process.l1tPh2NanoTask.add(p2GTL1TablesTask)
    return process

### Main Ph2L1 objects
from PhysicsTools.L1Nano.l1tPh2Nanotables_cff import *
def addPh2L1Objects(process):
    process.l1tPh2NanoTask.add(p2L1TablesTask)
    return process

### Reco Jets
from PhysicsTools.NanoAOD.jetsAK4_Puppi_cff import *
def add_puppi_jets(process):
    jetPuppiTable.src = cms.InputTag("finalJetsPuppi")
    for var in ["nMuons", "muonIdx1", "muonIdx2", "electronIdx1", "electronIdx2", "nElectrons", "svIdx1", "svIdx2", "nSVs"]:
        delattr(jetPuppiTable.variables, var)

    process.l1tPh2NanoTask.add(jetPuppiTask)
    process.l1tPh2NanoTask.add(jetPuppiForMETTask)
    jetPuppiTablesTask = cms.Task(jetPuppiTable)
    process.l1tPh2NanoTask.add(jetPuppiTablesTask)

### Reco Taus
from PhysicsTools.NanoAOD.taus_cff import *
def add_taus(process):
    tauTable.src = cms.InputTag("finalTaus")
    for var in ["jetIdx", "eleIdx", "muIdx", "svIdx1", "svIdx2", "nSVs"]:
        delattr(tauTable.variables, var)

    process.l1tPh2NanoTask.add(finalTaus)
    tauTablesTask = cms.Task(tauTable)
    process.l1tPh2NanoTask.add(tauTablesTask)


#### GENERATOR INFO
## based on https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/nanogen_cff.py#L2-L36
from PhysicsTools.NanoAOD.genparticles_cff import * ## for GenParts
from PhysicsTools.NanoAOD.jetMC_cff import * ## for GenJets
from PhysicsTools.NanoAOD.met_cff import metMCTable ## for GenMET
from PhysicsTools.NanoAOD.globals_cff import puTable ## for PU
#from PhysicsTools.NanoAOD.taus_cff import * ## for Gen taus
def addGenObjects(process):

    ## add more GenVariables
    # from L1Ntuple Gen: https://github.com/artlbv/cmssw/blob/94a5ec13b8ce76afb8ea4f157bb92fb547fadee2/L1Trigger/L1TNtuples/plugins/L1GenTreeProducer.cc#L203
    genParticleTable.variables.vertX = Var("vertex.x", float, "vertex X")
    genParticleTable.variables.vertY = Var("vertex.y", float, "vertex Y")
    genParticleTable.variables.vertZ = Var("vertex.z", float, "vertex Z")
    genParticleTable.variables.lXY = Var("sqrt(vertex().x() * vertex().x() + vertex().y() * vertex().y())", float, "lXY")
    genParticleTable.variables.dXY = Var("-vertex().x() * sin(phi()) + vertex().y() * cos(phi())", float, "dXY")

    ## add pruned gen particles a la Mini
    if False:
        ## Gen all
        # genParticleTable.src = "genParticles" # see
        ## Mini default, see  https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatAlgos/python/slimming/prunedGenParticles_cfi.py
        # genParticleTable.src = "prunedGenParticles"
        ## Nano default, see https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/genparticles_cff.py#L8
        # genParticleTable.src = "finalGenParticles"

        process.prunedGenParticleTable = genParticleTable.clone()
        process.prunedGenParticleTable.src = "prunedGenParticles"
        process.prunedGenParticleTable.name = "prunedGenPart"
        process.l1tPh2NanoTask.add(process.prunedGenParticleTable)

    # lower genVisTau pt threshold
    process.genVisTauTable.cut = "pt > 1"
    # lower AK8 gen jet threshold
    process.genJetAK8Table.cut = "pt > 10"

    process.l1tPh2NanoTask.add(
                puTable, metMCTable,
                genParticleTask, genParticleTablesTask,
                genTauTask,
    )

    # add all GenJets: AK4 and AK8
    process.l1tPh2NanoTask.add(genJetTable,patJetPartonsNano,genJetFlavourTable)
    process.l1tPh2NanoTask.add(genJetAK8Table,genJetAK8FlavourAssociation,genJetAK8FlavourTable)

    return process

from PhysicsTools.NanoAOD.triggerObjects_cff import *
def add_trig_objects(process):
    process.l1tPh2NanoTask.add(unpackedPatTrigger)
    process.l1tPh2NanoTask.add(triggerObjectTable)

def addFullPh2L1Nano(process):
    addGenObjects(process)
    addPh2L1Objects(process)
    addPh2GTObjects(process)
    add_puppi_jets(process)
    add_taus(process)
    add_trig_objects(process)

    return process





import os
import time
import random
import string
import sys
import json
from copy import deepcopy as copy

dict_format = True
resub_wall_time = 2000
cmnd = None
options = None
maxlen = 30


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def randomize(input_string):
    random_str = "".join(random.choice(string.ascii_letters) for _ in range(10))
    return "{}_{}".format(input_string, random_str)


status_d = {}

def auto_resubmitter(lines):
    max_memory_val = 0
    mem_tag = "RSS="
    killed_job_tag = "wall clock limit"
    was_killed = False
    for line in lines:
        index = line.find(mem_tag)
        if index != -1:  # found!
            mem_val = int(line[index + len(mem_tag):].split(" ")[0])
            if mem_val > max_memory_val:
                max_memory_val = mem_val
        if line.find(killed_job_tag) != -1:
            was_killed = True
    return min(max_memory_val, 5000), was_killed


def run_status(names):
    new_names = copy(names)
    niter = -1
    while True:
        niter += 1
        if niter > int(options.niterations) and int(options.niterations) > 0:
            break
        names = copy(new_names)
        for name in names:
            # if "scenarioA" not in name:
                # continue
            r = randomize("tmp")
            if not os.path.exists(cmnd.format(name=name)):
                continue
            if options.kill:
                os.system("crab kill -d {}".format(cmnd.format(name=name)))
                continue
            os.system("crab status -d {} > {}".format(cmnd.format(name=name), r))

            with open(r) as f:
                lines = f.readlines()
            os.system("rm %s" % r)
            if "CMSSW is missing. You must do cmsenv first" in lines[0]:
                print(lines[0])
                sys.exit()

            if options.invalidate:
                dataset = None
                for line in lines:
                    if "Output dataset" in line:
                        line = line.strip().split("\t")
                        dataset = line[-1]
                        break
                if dataset:
                    os.system(f"crab-dev setfilestatus --status INVALID --dataset {dataset}")
                    continue

            if options.dataset:
                dataset = None
                for line in lines:
                    if "Output dataset" in line:
                        line = line.strip().split("\t")
                        dataset = line[-1]
                        break
                if dataset:
                    if not dict_format:
                        print(f"{name}: {dataset}")
                    else:
                        print(f'"{name}": "{dataset}",')
                else:
                    print("No dataset info for %s" % name)
                continue

            status = {
                "running": 0,
                "idle": 0,
                "finished": 0,
                "transferring": 0,
                "failed": 0,
                "killed": 0,
                "done": 0,
            }
            for line in lines:
                line = line.replace("\t", "  ")
                for key in status:
                    if key + "  " in line:
                        status[key] = int(line.split("(")[-1].split("/")[0])

            if status["finished"] > 0 and status["done"] == status["finished"] and sum([st for st in status.values()]) == 2 * status["finished"]:
                print("%s%s finished.%s" % (bcolors.OKGREEN, name, bcolors.ENDC))
                new_names.remove(name)
                continue

            if options.end:
                continue

            run_status = "{:>3d}".format(status["running"])
            if status["running"] > 0:
                run_status = bcolors.OKBLUE + run_status + bcolors.ENDC

            fin_status = "{:>3d}".format(status["finished"])
            if status["finished"] > 0:
                fin_status = bcolors.OKGREEN + fin_status + bcolors.ENDC

            print("{name:<{size}s}: idle:{idle:>3d}, running:{run}, transferring:{transf:>3d}, finished:{fin} (transf:{done:>3d})".format(
                name=name, size=maxlen, idle=status["idle"], run=run_status, transf=status["transferring"], fin=fin_status, done=status["done"]
            ), end=""),
            if status["failed"] > 0 or status["killed"] > 0:
                print(", {}FAILED:{:>3d}{}".format(bcolors.FAIL, status["failed"] + status["killed"], bcolors.ENDC))
                print("Some job(s) failed. Try running {}crab status -d {} --verboseErrors{}".format(
                    bcolors.BOLD, cmnd.format(name=name), bcolors.ENDC))
                if options.resubmit:
                    os.system("crab resubmit -d {} --maxmemory=5000 --maxjobruntime=2000".format(cmnd.format(name=name)))

                if options.auto_resubmit:
                    os.system("crab status -d {} --verboseErrors > {}".format(cmnd.format(name=name), r))
                    with open(r) as f:
                        lines = f.readlines()
                    os.system("rm %s" % r)
                    max_memory_val, was_killed = auto_resubmitter(lines)
                    if max_memory_val != 0 or was_killed:
                        cmd = "crab resubmit -d {}".format(cmnd.format(name=name))
                        if max_memory_val != 0:
                            cmd += f" --maxmemory={max_memory_val + 250}"
                        if was_killed:
                            cmd += f" --maxjobruntime={resub_wall_time}"
                        print("--> Running " + cmd)
                        os.system(cmd)
            else:
                print()

            status_d[name] = status

        if any([options.dataset, options.resubmit, options.end, options.kill, options.invalidate]):
            break

        outname = "_".join(options.folder.split("/"))
        if outname.endswith("_"):
            outname = outname[:-1]
        with open(outname + ".json", "w+") as f:
            json.dump(status_d, f, indent=4)

        if len(new_names) == 0:
            print("All jobs are finished.")
            break
        print(f"Waiting for {options.sleep} minute{'s' if int(options.sleep) > 1 else ''}...")
        time.sleep(int(options.sleep) * 60)
    
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--folder', dest='folder', default='')
    parser.add_argument('-d','--dataset', action='store_true', default=False)
    parser.add_argument('-r','--resubmit', action='store_true', default=False)
    parser.add_argument('-e','--end', action='store_true', default=False)
    parser.add_argument('-k','--kill', action='store_true', default=False)
    parser.add_argument('-i','--invalidate', action='store_true', default=False)
    parser.add_argument('-auto','--auto-resubmit', action='store_false', default=True)
    parser.add_argument('-n','--names', dest='names', default='')
    parser.add_argument('-s', '--sleep', dest='sleep', default='1')
    parser.add_argument('-iter', '--niterations', dest='niterations', default='-1')
    options = parser.parse_args()

    p = "/afs/cern.ch/work/j/jleonhol/private/samplegeneration/CMSSW_10_6_43/src/Configuration/GenProduction/data"
    files = os.listdir(p)
    names = options.names.split(",") if options.names else [f.split(".")[0] for f in files]

    cmnd = "%s/{name}/crab_{name}/" % options.folder
    #cmnd = "crab status -d %s/{name}_2022/crab_{name}_2022/" % options.folder
    maxlen = max([len(name) for name in names])
    
    run_status(names)

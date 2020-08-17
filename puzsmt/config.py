import json
import sys
# WOOO EVERY LOVES GLOBAL VARIABLES!!!


# let's put all our config into one variable because.. then we only have one global?


CONFIG = {
    # How many cores to use when running in parallel
    # Set to 1 (or 0) to disable parallelisation
    "parallel": 8,


    # How many times to try looking for each size of core
    "repeats": 3,

    # Encode "at most one thing is true" as a single clause
    "OneClauseAtMost": False,

    # Limit search to 100,000 conflicts
    "solveLimited": True
}



def LoadConfigFromDict(dict):
    global CONFIG
    for (k,v) in dict.items():
        if k not in CONFIG:
            print("Invalid CONFIG option: " + k)
            sys.exit(1)
        CONFIG[k] = v

def LoadConfigFromFile(file):
    with open(file) as f:
        data = json.load(f)
        LoadConfigFromDict(data)

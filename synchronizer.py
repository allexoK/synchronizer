from xml.dom import minidom
from synchFunctions import checkXml,loadCoreSignal,loadSignals,synchSignals
import argparse
import sys
import pandas as pd

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-o", "--output", help="Your csv output file.")
    parser.add_argument("-c", "--config", help="XML configuration file.")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options

options = getOptions(sys.argv[1:])

res = checkXml(options.config,options.verbose)
if(res["error"] == False):
    res = loadCoreSignal(options.config,options.verbose)
    coresignal = {
        "name":res["name"],
        "x":res["x"],
        "y":res["y"]
    }
if(res["error"] == False):
    signals = loadSignals(options.config,options.verbose)

if(res["error"] == False):
    res = synchSignals(coresignal,signals,options.verbose)

if(res["error"] == False):
    res.pop("error")
    if(options.output):
        if(options.verbose == True):
            print("Saving as \"" + options.output + "\"...")
        pd.DataFrame.from_dict(res).to_csv(options.output,index=False,sep=";")
    else:
        print("No output csv specified!!!")
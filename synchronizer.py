from xml.dom import minidom
from synchFunctions import checkXml,loadCoreSignal,loadSignals,synchSignals
import argparse
import sys
import pandas as pd

class synchronizer:
    def __init__(self,output,config,verbose):
        res = checkXml(config,verbose)
        if(res["error"] == False):
            res = loadCoreSignal(config,verbose)
            coresignal = {
                "name":res["name"],
                "Time":res["Time"],
                "y":res["y"]
            }
        if(res["error"] == False):
            signals = loadSignals(config,verbose)

        if(res["error"] == False):
            res = synchSignals(coresignal,signals,verbose)

        if(res["error"] == False):
            res.pop("error")
            ks = res.keys()
            for k in ks:
                print(k,len(res[k]))
            if(output):
                if(verbose == True):
                    print("Saving as \"" + output + "\"...")
                pd.DataFrame.from_dict(res).to_csv(output,index=False,sep=";")
            else:
                print("No output csv specified!!!")
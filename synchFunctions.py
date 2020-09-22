import pandas as pd
import argparse
import sys
from xml.dom import minidom
  
def checkXml(path,vrb):
    response = {}
    error = False
    mydoc = minidom.parse(path)
    items = mydoc.getElementsByTagName('config')
    if(len(items) == 1):
        if(vrb == True):
            print("Configuration node found in XML- OK")
        response["configFound"] = True
    else:
        if(vrb == True):
            print("Configuration node not found in XML- ERROR")
        response["configFound"] = False
        error = True
    items = mydoc.getElementsByTagName('coreSignal')
    if(len(items) == 1):
        if(vrb == True):
            print("Core signal node found in XML- OK")
        response["coreFound"] = True
    else:
        if(vrb == True):
            print("Core signal node not found in XML - ERROR")
        response["coreFound"] = False
        error = True
    items = mydoc.getElementsByTagName('signal')
    if (len(items) > 0):
        if(vrb == True):
            print("Found ",len(items)," signals in XML - OK")
    else:
        error = True
        if(vrb == True):
            print("No signals found in XML- ERROR")
    response["signal"] = len(items)
    response["error"] = error
    return response

def loadCoreSignal(path,vrb):
    mydoc = minidom.parse(path)
    response = {}
    error = False  
    items = mydoc.getElementsByTagName('coreSignal')
    if(len(items) == 1):
        name = items[0].attributes['name'].value
        filepath = items[0].getElementsByTagName('fp')[0].firstChild.data
        delim = items[0].getElementsByTagName('delim')[0].firstChild.data
        xIndex = int(items[0].getElementsByTagName('xIndex')[0].firstChild.data)
        yIndex = int(items[0].getElementsByTagName('yIndex')[0].firstChild.data)
        if(vrb == True):
            print("Core signal \"" +name+"\" loaded - OK")
    else:
        if(vrb == True):
            print("Core signal load error - ERROR")
        error = True
    if(error == False):
        df = pd.read_csv(filepath,delim)
        cols = list(df.columns)
        response["name"] = name
        response["Time"] = df[cols[xIndex]]
        response["y"] = df[cols[yIndex]]
    response["error"] = error
    return response

def loadSignals(path,vrb):
    mydoc = minidom.parse(path)
    response = {}
    sigs = []
    error = False  
    items = mydoc.getElementsByTagName('signal')
    for signal in items:
        sig = {}
        name = signal.attributes['name'].value
        filepath = signal.getElementsByTagName('fp')[0].firstChild.data
        delim = signal.getElementsByTagName('delim')[0].firstChild.data
        xIndex = int(signal.getElementsByTagName('xIndex')[0].firstChild.data)
        yIndex = int(signal.getElementsByTagName('yIndex')[0].firstChild.data)

        df = pd.read_csv(filepath,delim)
        cols = list(df.columns)
        sig["name"] = name
        sig["Time"] = df[cols[xIndex]]
        sig["y"] = df[cols[yIndex]]
        sigs.append(sig)
        if(vrb == True):
            print("Signal \"" + name + "\" loaded")
    return sigs

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

def synchSignals(core,sig,vrb):
    newSigs = {
        "Time":[],
        core["name"]:[]
    }
    for s in sig:
        s["ctr"] = 0 
        newSigs[s["name"]] = []
    
    if(vrb == True):
        print("Synchronizing signals...")

    iters = len(core["Time"])
    for i in range(1,len(core["Time"])):
        if (i%100 == 0):
            printProgressBar(i,iters)
        timeToLookUpHigh = core["Time"][i]
        timeToLookUpLow = core["Time"][i-1]
        newSigs["Time"].append(timeToLookUpLow)
        newSigs[core["name"]].append(core["y"][i])
        for i in range(len(sig)):# check all signals if current elements to find has the same time as current core time
            currentSignalCtr = sig[i]["ctr"]
            if(currentSignalCtr < len(sig[i]["Time"])):#if there are still unprocessed values of signals
                timeOfNextEl = sig[i]["Time"][currentSignalCtr]
                while(timeOfNextEl < timeToLookUpLow and currentSignalCtr < len(sig[i]["Time"])):# move time of sig to make it bigger than current core time
                    sig[i]["ctr"] += 1
                    timeOfNextEl = sig[i]["Time"][currentSignalCtr]
                    currentSignalCtr = sig[i]["ctr"]
                if(currentSignalCtr < len(sig[i]["Time"])):# if signal is not finished yet
                    if(timeOfNextEl <= timeToLookUpHigh):# if the signal time is in frame timeToLookUpLow and timeToLookUpHigh add it to final signal
                        valueOfSigToSynch = sig[i]["y"][currentSignalCtr]
                        newSigs[sig[i]["name"]].append(valueOfSigToSynch)
                        sig[i]["ctr"] += 1
                    else:
                        newSigs[sig[i]["name"]].append(None)# if signal time is not in frame timeToLookUpLow and timeToLookUpHigh add None to final signal and wait for next core time
                else:
                    newSigs[sig[i]["name"]].append(None) # if signal is finished add None to its column in he output
            else:
                newSigs[sig[i]["name"]].append(None)# if signal is finished add None to its column in he output
    printProgressBar(iters,iters)
    newSigs["error"] = False
    return newSigs
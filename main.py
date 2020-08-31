import os
import sys
import argparse
from configCreator import ConfigCreator
import pandas as pd

confToCreateName = "confC.xml"
def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-f", "--fixation", help="Fixation file.")
    parser.add_argument("-g", "--gaze", help="Gaze file.")
    parser.add_argument("-o", "--odboceni", help="Odboceni file.")
    parser.add_argument("-e", "--ekg", help="Ekg file.")
    parser.add_argument("-out", "--outputFile", help="Your ouput csv file.")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options

options = getOptions(sys.argv[1:])

convertDicomToCsv = "python3 dicomReader.py -i " + options.ekg + " -o ekgGen.csv"
timeShiftEkg = "python3 timeShifter.py -i ekgGen.csv -d \";\" -c 0 -t 7205753 -o ekg.csv"
timeShiftOdboceni = "python3 timeShifter.py -i " + options.odboceni + " -d \" \" -c 0 -t 7189616 -o odboceni.csv"
deleteRepeatedTimebaseValues = "python3 repeatedValuesDeleter.py -i odboceni.csv -d \";\" -c 0 -o odboceni.csv"
synchronizeData = "python3 synchronizer.py -c "+ confToCreateName +" -o " + options.outputFile

if(options.verbose == True):
    convertDicomToCsv += " -v"
    timeShiftEkg += " -v"
    timeShiftOdboceni += " -v"
    deleteRepeatedTimebaseValues += " -v"
    synchronizeData += " -v"

df = pd.read_csv("odboceni.csv",delimiter=";")
keys = df.keys()

cc = ConfigCreator(confToCreateName,"odboceni.csv",";","0","1",keys[1])

for i in range(2,len(keys)):
    cc.addColumnsFromFile("odboceni.csv",";","0",str(i),keys[i])

df = pd.read_csv("ekg.csv",delimiter=";")
keys = df.keys()
for i in range(1,len(keys)):
    cc.addColumnsFromFile("ekg.csv",";","0",str(i),keys[i])

df = pd.read_csv(options.fixation,delimiter=";")
keys = df.keys()
for i in range(1,len(keys)):
    cc.addColumnsFromFile(options.fixation,";","0",str(i),keys[i])

df = pd.read_csv(options.gaze,delimiter=";")
keys = df.keys()
for i in range(1,len(keys)):
    cc.addColumnsFromFile(options.gaze,";","0",str(i),keys[i])


#Creates xml configurator based on 
cc.createFile()

os.system(convertDicomToCsv)
os.system(timeShiftEkg)
os.system(timeShiftOdboceni)
os.system(deleteRepeatedTimebaseValues)
os.system(synchronizeData)

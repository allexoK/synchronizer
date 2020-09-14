import os
import sys
import argparse
from dicomReader import dicomReader
from timeShifter import timeShifter
from repeatedValuesDeleter import repeatedValuesDeleter
from synchronizer import synchronizer
from configFileCreator import configFileCreator
if(os.path.isdir("temp") == False):
    os.mkdir("temp")

confToCreateName = "temp/confC.xml"
def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-f", "--fixation", help="Fixation file.")
    parser.add_argument("-g", "--gaze", help="Gaze file.")
    parser.add_argument("-o", "--simulator", help="Odboceni file.")
    parser.add_argument("-e", "--ecg", help="Ekg file.")
    parser.add_argument("-out", "--outputFile", help="Your ouput csv file.")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options

options = getOptions(sys.argv[1:])

dicomReader(options.ecg,"temp/ekgGen.csv",True)
timeShifter("temp/ekgGen.csv",";","0","7205753","temp/ekg.csv",True)
timeShifter(options.simulator," ","0","7189616","temp/odboceni.csv",True)
configFileCreator(confToCreateName,options.fixation,options.gaze)
repeatedValuesDeleter("temp/odboceni.csv",";","0","temp/odboceni.csv",True)
synchronizer(options.outputFile,confToCreateName,True)
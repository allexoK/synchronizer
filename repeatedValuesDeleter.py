import argparse
import sys
import pandas as pd


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-i", "--input", help="Your input file.")
    parser.add_argument("-d", "--delimiter", help="Delimiter of input file.")
    parser.add_argument("-c", "--columnIndex", help="Index of timebase.")
    parser.add_argument("-o", "--outputFile", help="Your ouput csv file.")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options


options = getOptions(sys.argv[1:])
if(options.verbose == True):
    print("Checking for repeated timebase values for timebase with index "+options.columnIndex+" in file \""+ options.input + "\"")

df = pd.read_csv(options.input,options.delimiter)
colName = df.keys()[int(options.columnIndex)]

timeBase = df[colName]
indexesToDrop = []

iters = len(timeBase)
for i in range(1,iters):
    if(i%10 == 0):
        printProgressBar(i,iters)
    if(timeBase[i] == timeBase[i-1]):
        # print(timeBase[i],timeBase[i-1])
        indexesToDrop.append(i)

if(len(indexesToDrop) == 0):
    if(options.verbose == True):
        print("No repeated time values found")
else:
    if(options.verbose == True):
        print(str(len(indexesToDrop)) + " repeated time values found")
    df.drop(index = indexesToDrop,inplace = True)
if(options.verbose == True):
     print("Saving modified file to \""+ options.outputFile + "\"")

df.to_csv(options.outputFile,";",index=False)
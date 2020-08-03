import argparse
import sys
import pandas as pd

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-i", "--input", help="Your input file.")
    parser.add_argument("-d", "--delimiter", help="Delimiter of input file.")
    parser.add_argument("-c", "--columnIndex", help="Index of column to shift.")
    parser.add_argument("-t", "--time", help="Shift time.")
    parser.add_argument("-o", "--outputFile", help="Your ouput csv file.")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options


options = getOptions(sys.argv[1:])
if(options.verbose == True):
    print("Shifting column with index "+options.columnIndex+" in file \""+ options.input + "\" with time " + options.time)

def modifyVal(val):
    val+=int(options.time)
    return val

df = pd.read_csv(options.input,options.delimiter)
colName = df.keys()[int(options.columnIndex)]
df[colName] = df[colName].apply(modifyVal)

if(options.verbose == True):
    print("Saving time-shifted data to file \""+ options.outputFile + "\"")

df.to_csv(options.outputFile,";",index=False)
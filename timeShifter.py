import argparse
import sys
import pandas as pd

class timeShifter:
    def __init__(self,inputFile,delimiter,columnIndex,time,outputFile,verbose):

        if(verbose == True):
            print("Shifting column with index "+columnIndex+" in file \""+ inputFile + "\" with time " + time)

        def modifyVal(val):
            val+=int(time)
            return val

        df = pd.read_csv(inputFile,delimiter)
        colName = df.keys()[int(columnIndex)]
        df[colName] = df[colName].apply(modifyVal)

        if(verbose == True):
            print("Saving time-shifted data to file \""+ outputFile + "\"")

        df.to_csv(outputFile,";",index=False)
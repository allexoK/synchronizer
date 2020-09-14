import argparse
import sys
import pandas as pd

class repeatedValuesDeleter:
    def __init__(self,inputFile,delimiter,columnIndex,outputFile,verbose):
        if(verbose == True):
            print("Checking for repeated timebase values for timebase with index "+columnIndex+" in file \""+ inputFile + "\"")

        df = pd.read_csv(inputFile,delimiter)
        colName = df.keys()[int(columnIndex)]
        timeBase = df[colName]
        indexesToDrop = []
        iters = len(timeBase)
        for i in range(1,iters):
            if(i%10 == 0):
                self.printProgressBar(i,iters)
            if(timeBase[i] == timeBase[i-1]):
                # print(timeBase[i],timeBase[i-1])
                indexesToDrop.append(i)
        if(len(indexesToDrop) == 0):
            if(verbose == True):
                print("No repeated time values found")
        else:
            if(verbose == True):
                print(str(len(indexesToDrop)) + " repeated time values found")
            df.drop(index = indexesToDrop,inplace = True)
        if(verbose == True):
             print("Saving modified file to \""+ outputFile + "\"")
        df.to_csv(outputFile,";",index=False)

    def printProgressBar (self,iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        if iteration == total: 
            print()



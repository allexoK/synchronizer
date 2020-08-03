from pydicom import dcmread
import pandas as pd
import struct
import datetime
import argparse
import sys
import pandas as pd

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-i", "--input", help="Your input dcm file.")
    parser.add_argument("-o", "--outputFile", help="Your ouput csv file.")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options

options = getOptions(sys.argv[1:])
if(options.verbose == True):
    print("Opening dicom...")

ds = dcmread(options.input)
data = ds[0x5400, 0x0100][0][0x5400, 0x1010]
time = ds[0x0008,0x002a].value
year = int(time[0:4])
month = int(time[4:6])
day = int(time[6:8])
hour = int(time[8:10])
minute = int(time[10:12])
sec = int(time[12:14])
time = datetime.datetime(year,month,day,hour,minute,sec,0).timestamp()*1000

pdData = []
for offset in range(0,len(data.value),24) :
    pdData.append(int(time+(offset/24)*2))    

df = pd.DataFrame(pdData,columns = ["time"])

pdData0 = []
pdData1 = []
pdData2 = []
pdData3 = []
pdData4 = []
pdData5 = []
pdData6 = []
pdData7 = []
pdData8 = []
pdData9 = []
pdData10 = []
pdData11 = []

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

if(options.verbose == True):
    print("Reading \""+ options.input +"\"")

iters = len(data.value)
for offset in range(0,len(data.value),24) :
    if(offset % 100 == 0):
        printProgressBar(offset,iters)
    pdData0.append(struct.unpack_from("h",data.value,offset)[0])
    pdData1.append(struct.unpack_from("h",data.value,offset+2)[0])
    pdData2.append(struct.unpack_from("h",data.value,offset+4)[0])
    pdData3.append(struct.unpack_from("h",data.value,offset+6)[0])
    pdData4.append(struct.unpack_from("h",data.value,offset+8)[0])
    pdData5.append(struct.unpack_from("h",data.value,offset+10)[0])
    pdData6.append(struct.unpack_from("h",data.value,offset+12)[0])
    pdData7.append(struct.unpack_from("h",data.value,offset+14)[0])
    pdData8.append(struct.unpack_from("h",data.value,offset+16)[0])
    pdData9.append(struct.unpack_from("h",data.value,offset+18)[0])
    pdData10.append(struct.unpack_from("h",data.value,offset+20)[0])
    pdData11.append(struct.unpack_from("h",data.value,offset+22)[0])

printProgressBar(iters,iters)

df["Ecg1"]=pdData0
df["Ecg2"]=pdData1
df["Ecg3"]=pdData2
df["Ecg5"]=pdData3
df["Ecg6"]=pdData4
df["Ecg7"]=pdData5
df["Ecg8"]=pdData6
df["Ecg9"]=pdData7
df["Ecg10"]=pdData8
df["Ecg11"]=pdData10
df["Ecg12"]=pdData11

if(options.verbose == True):
    print("Saving \""+ options.outputFile + "\"")

df.to_csv(options.outputFile,sep=';',index=False)

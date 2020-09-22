from configCreator import ConfigCreator
import pandas as pd

class configFileCreator:
    def __init__(self,confToCreateName,fixation,gaze):
        df = pd.read_csv("temp/odboceni.csv",delimiter=";")
        keys = df.keys()

        newKeys = ["Time", "X", "Y", "Z", "Xrot", "Yrot", "Zrot", "Speed", "Accelerator", "Break", "Clutch", "Wheel", "Handbreak", "Gear", "Winker", "Wiper", "Buttons"]
        keys = newKeys
        cc = ConfigCreator(confToCreateName,"temp/odboceni.csv",";","0","1",keys[1])

        for i in range(2,len(keys)):
            cc.addColumnsFromFile("temp/odboceni.csv",";","0",str(i),keys[i])

        df = pd.read_csv("temp/ekg.csv",delimiter=";")
        keys = df.keys()
        for i in range(1,len(keys)):
            cc.addColumnsFromFile("temp/ekg.csv",";","0",str(i),keys[i])

        df = pd.read_csv(fixation,delimiter=";")
        keys = df.keys()
        for i in range(1,len(keys)):
            cc.addColumnsFromFile(fixation,";","0",str(i),keys[i])

        df = pd.read_csv(gaze,delimiter=";")
        keys = df.keys()
        for i in range(1,len(keys)):
            cc.addColumnsFromFile(gaze,";","0",str(i),keys[i])
        #Creates xml configurator based on 
        cc.createFile()

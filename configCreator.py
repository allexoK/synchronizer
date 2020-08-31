import xml.etree.cElementTree as ET

class ConfigCreator:
    def __init__(self,configFileName,coreSignalInputFilePath,coreSignalInputFileDelimiter,coreSignalXIndex,coreSignalYIndex,coreSignalNewName):
        self.configFileName = configFileName
        self.root = ET.Element("config")
        coresig = ET.SubElement(self.root, "coreSignal",name=coreSignalNewName)

        ET.SubElement(coresig, "fp").text = coreSignalInputFilePath
        ET.SubElement(coresig, "delim").text = coreSignalInputFileDelimiter
        ET.SubElement(coresig, "xIndex").text = coreSignalXIndex
        ET.SubElement(coresig, "yIndex").text = coreSignalYIndex


    def addColumnsFromFile(self,signalPath,signalDelimiter,signalXIndex,signalYIndex,signalNewName):
        sig = ET.SubElement(self.root, "signal",name=signalNewName)
        ET.SubElement(sig, "fp").text = signalPath
        ET.SubElement(sig, "delim").text = signalDelimiter
        ET.SubElement(sig, "xIndex").text = signalXIndex
        ET.SubElement(sig, "yIndex").text = signalYIndex


    def createFile(self):
        tree = ET.ElementTree(self.root)
        tree.write(self.configFileName)

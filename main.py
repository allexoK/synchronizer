import os

convertDicomToCsv = "python3 dicomReader.py -i ekg.dcm -o ekgGen.csv -v"
timeShiftEkg = "python3 timeShifter.py -i ekgGen.csv -d \";\" -c 0 -t 7205753 -o ekg.csv -v"
timeShiftOdboceni = "python3 timeShifter.py -i odboceni.txt -d \" \" -c 0 -t 7189616 -o odboceni.csv -v"
synchronizeData = "python3 synchronizer.py -c config.xml -o out.csv -v"

os.system(convertDicomToCsv)
os.system(timeShiftEkg)
os.system(timeShiftOdboceni)
os.system(synchronizeData)

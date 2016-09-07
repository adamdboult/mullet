##########
# Import #
##########
import os
import socket

import zipfile
import tarfile

import datetime
from operator import itemgetter
from basicFuncs import *

##################
# Unzip function #
##################
def unZip(data):
    print ("unz")
    print (data)
    paths = data["inputs"][0]
    print (paths)
    filePath = joinFolder(paths)
    outpath = os.path.dirname(filePath)
        
    if (filePath.endswith(".zip")):
        fh = open(filePath, 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            z.extract(name, outpath)
        fh.close()

    elif (filePath.endswith(".tar.gz")):
        tar =  tarfile.open(filePath, "r:gz")
        tar.extractall()
        tar.close()

    elif (filePath.endswith(".tar")):
        tar =  tarfile.open(filePath, "r:")
        tar.extractall()
        tar.close()
        
    else:
        pass

###############
# Expand file #
###############
def expandFile(data):
    print ("EXPANDING")
    rawLines = data["inputs"][0]
    paths = data["inputs"][1]
    pre = data["inputs"][2]

    expandPath = joinFolder(paths)
    
    results = []
    with open (expandPath) as expandFile:
        expandLines = expandFile.read().splitlines()
        for rawLine in rawLines:
            for expandLine in expandLines:
                if (pre=="true"):
                    candidate = expandLine + rawLine
                else:
                    candidate = rawLine + expandLine
                candidate = candidate.replace("\n","")+"\n"
                results.append(candidate)
    return results

################
# Get hostname #
################
def getHostName(data):
    rawLine = socket.gethostname()
    return [rawLine]

###############
# Filter file #
###############
def filterFile(data):
    rawLines = data["inputs"][0]
    paths = data["inputs"][1]

    filterPath = joinFolder(paths)
    results = []
    with open (filterPath) as filterFile:
        filterLines = filterFile.read().splitlines()
        for rawLine in rawLines:
            write = 1
            for filterLine in filterLines:
                if (filterLine.strip() == rawLine.strip()):
                    write = 0
            if (write == 1):
                results.append(rawLine)

        return results

##########
# To MP3 #
##########
def toMP3(data):
    paths = data["inputs"][0]

    filePath = joinFolder(paths)
    newPath = os.path.splitext(filePath)[0]+".mp3"
    
    commandArray = ["ffmpeg", "-i ", filePath, "-qscale:a", "0", newPath]
    runSys([commandArray])
    
############
# OwnQuant #
############
def ownQuant(data):
    inputDir = data["tempFolder"]

    thisRegex = "^.*\.csv$"
    fileArray = getMatchContents(data["tempFolder"], "localhost", thisRegex)
    for filePath in fileArray:
        writePath = folderpath + "ALL"+foldername + ".csv"

        skipRow = 0
        if (fileExists):
            skipRow = 1

        appendFile(data, filePath, writePath, skipRow, 0)

    thisRegex = "^ALL.*\.csv$"
    fileArray = getMatchContents(data["tempFolder"], "localhost", thisRegex)

    for filePath in fileArray:
        confName = folderpath + foldername +".conf"
        outputName =folderpath + "OUT" + foldername + ".csv"

        with open (inputName, "r") as inputFile:
            inputRows = inputFile.splitrows()
            with open(confName, 'rb') as confFile:
                confRows = fileConf.read().splitlines()
                # load date format
                with open(outputName, "w") as outputFile:
                    # correct date format
                    # sort by date format

                    #process top row, start at 2nd
                    for inputRow in inputRows:
                        inputRow[0] = datetime.datetime.strptime(row[0], "%d/%m/%Y")
                        inputRow[0] = row[0].strftime("%d/%m/%Y")
            
                        newValue = ""
                        # skip first two, process?
                        for confRow in confRows:
                            confArray = confRow.split(',')
                            dataType = confArray[0]
                            if (dataType == "date"):
                                newValue = testSplit[int(confArray[1])]
                                newValue = datetime.datetime.strptime(newValue, confRows[1]).strftime("%d/%m/%Y")
                            elif (dataType == "copy"):
                                newValue = testSplit[int(confArray[1])]
                            elif (dataType == "divide"):
                                newValue = float(testSplit[int(confArray[1])]) / float(testSplit[int(confArray[2])])
                            elif (dataType == "weight"):
                                newValue = 0
                            for k in range (1, len(confArray), 2):
                                newValue = newValue + float(testSplit[int(confArray[k])]) * float(confArray[k + 1])

                            if (toAdd == ""):
                                toAdd = str(newValue)
                            else:
                                toAdd = toAdd + ',' + str(newValue)
                                
                        outputRows.append(toAdd)

                    outputRows.sort(key=itemgetter(0))  # sort by the datetime column
                    for outputRow in outputRows:
                        fileOutput.write("%s\n" % stringOut)

    fileArray = getMatchContents(data["tempFolder"], "localhost", thisRegex)
    for filePath in fileArray:
        systemScript = ("do gnuplot")
        os.sys(systemScript)

##########
# Import #
##########
import os
import socket

import zipfile
import tarfile
import shlex

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
    
    outpath = os.path.splitext(filePath)[0]
    #outpath = joinFolder(os.path.dirname(filePath), os.path.basename(filePath))
    
    if (filePath.endswith(".zip")):
        fh = open(filePath, 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            z.extract(name, outpath)
        fh.close()

    elif (filePath.endswith(".tar.gz")):
        tar =  tarfile.open(filePath, "r:gz")
        tar.extractall(outpath)
        tar.close()

    elif (filePath.endswith(".tar")):
        tar =  tarfile.open(filePath, "r:")
        tar.extractall(outpath)
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

###########
# Install #
###########
def install(data):
    programs = data["inputs"][0]

    for program in programs:
        commandString = "sudo apt-get -y install " + program.replace("\n","")
        print (commandString)
        commandArray = shlex.split(commandString)
        data["inputs"][0]=commandArray
        runSys(data)

##########
# To MP3 #
##########
def toMP3(data):
    paths = data["inputs"][0]

    filePath = joinFolder(paths)
    newPath = os.path.splitext(filePath)[0]+".mp3"

    filePath = escapeString(filePath)
    newPath = escapeString(newPath)

    commandString = "ffmpeg -i " + filePath + " -qscale:a 0 " + newPath
    print (commandString)

    commandArray = shlex.split(commandString)
    data["inputs"][0]=commandArray
    runSys(data)
    
############
# OwnQuant #
############
# look all files
# copy all files to temp
# look for all csv files
# make ALLaldermore.csv etc (if exists, skip 1)
# find all ALLetc.csv
# for each, find matching conf
def ownQuant(data):
    inputDir = data["inputs"][0]
    tempFolder = data["tempFolder"]
    thisRegex = "csv"

    data["inputs"] = ["f", "false", "false", [inputDir], "localhost", [thisRegex]]

    fileArray = getMatchContents(data)
    allPaths = []
    for filePath in fileArray:
        split = filePath.split("/")
        baseFolder = split[len(split)-2]
        dirname = os.path.dirname(filePath)
        writePath = joinFolder([tempFolder, dirname, "ALL" + baseFolder +".csv"])
        if (writePath in allPaths):
            skipRow = 1
        else:
            allPaths.append(writePath)
            skipRow = 0

        data["inputs"] = [[data["tempFolder"],filePath], skipRow, 0]

        lines = readFile(data)
    
        data["inputs"] = [lines, [writePath]]
        appendFile(data)
    thisRegex = "ALL"
    data["inputs"] = ["f", "false", "false", [inputDir], "localhost", [thisRegex]]
    fileArray = getMatchContents(data)
    for filePath in fileArray:

        split = filePath.split("/")
        baseFolder = split[len(split)-2]

        dirname = os.path.dirname(filePath)
        confName = joinFolder([tempFolder, dirname, "conf.conf"])
        inputName = joinFolder([tempFolder, filePath])
        outputName = joinFolder([tempFolder, dirname, "OUT" + baseFolder +".csv"])
        ### I'M UP TO HERE
        with open (inputName, "r") as inputFile:
            inputRows = inputFile.readlines()
            with open(confName, 'rb') as confFile:
                confRowsRaw = confFile.readlines()
                confRows =[]
                for row in confRowsRaw:
                    confRows.append(str(row, 'utf-8').replace("\n",""))
                
                with open(outputName, "w") as outputFile:
                    # SORT BY DATE FORMAT
                    outputRows = [confRows[2]]
                    i = 0
                    j = 0
                    for inputRow in inputRows:
                        inputRow = inputRow.replace("\n","")
                        inputArray = inputRow.split(",")
                        if (i == 0):
                            i = 1
                        else:
                            newValue = ""
                            j = 0
                            toAdd = ""
                            print (confRows)
                            for confRow in confRows:
                                if (j > 2):
                                    confArray = confRow.split(',')
                                    dataType = confArray[0]
                                    if (dataType == "date"):
                                        newValue = inputArray[int(confArray[1])]
                                        newValue = datetime.datetime.strptime(newValue, confRows[1])
                                        newValue = datetime.datetime.strftime(newValue, "%d/%m/%Y")
                                    elif (dataType == "copy"):
                                        newValue = inputArray[int(confArray[1])]
                                    elif (dataType == "divide"):
                                        newValue = float(inputArray[int(confArray[1])]) / float(inputArray[int(confArray[2])])
                                    elif (dataType == "weight"):
                                        newValue = 0
                                        for k in range (1, len(confArray), 2):
                                            newValue = newValue + float(inputArray[int(confArray[k])]) * float(confArray[k + 1])

                                    if (toAdd == ""):
                                        toAdd = str(newValue)
                                    else:
                                        toAdd = toAdd + ',' + str(newValue)
                                j = j + 1
                            outputRows.append(toAdd)
                        i = 1
                    print ("HERE WE ARE")
                    print (outputRows)
                    print ("half")
                    sortRows = outputRows[1:]
                    sortRows.sort(key=itemgetter(0))  # sort by the datetime column
                    sortRows.insert(0, outputRows[0])
                    
                    print (outputRows)
                    print ("DONE")
                    for outputRow in outputRows:
                        outputFile.write("%s\n" % outputRow)

    print ("S DELTA")
    thisRegex = "OUT"
    data["inputs"] = ["f", "start", "false", [inputDir], "localhost", [thisRegex]]
    fileArray = getMatchContents(data)
    for filePath in fileArray:
        outputPath = joinFolder([tempFolder,os.path.dirname(filePath),"graph.png"])
        inputPath = joinFolder([tempFolder, filePath])
        commandString = "gnuplot -e \"filename='" + inputPath+"'\" -e \"outputpath='" + outputPath+"'\" /home/adam/Projects/mullet/gnuplot.gp"
        print (commandString)
        data["inputs"] = [shlex.split(commandString)]

        runSys(data)

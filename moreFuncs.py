##########
# Import #
##########
import os
import socket
import sys

import urllib.request

import zipfile
import tarfile
import shlex

import datetime
from operator import itemgetter
from basicFuncs import *
import csv

##################
# Unzip function #
##################
def unZip(data):
    print ("unz")
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
    rawLine = socket.gethostname()+"\n"
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

#############
# Git clone #
#############
def gitClone(data):
    gitArray = data["inputs"][0]
    print ("GIT")
    print (gitArray)
    for git in gitArray:
        print ()
        print ("NEW")
        print (git)
        git = git.split("\t")
        if (len(git) > 1):
            URL = git[0].replace("\n", "")
            user = git[2]
            print ("B: " + URL)
            sourceArray = URL.split("/")
            filename = sourceArray[len(sourceArray) - 1]
            filename = filename.split(".")[0]
            
            destName = os.path.join(git[1], filename)
            commandString = "git clone " + URL + " " + destName
            print ("C: " + destName)
            print ("DA: " + commandString)
            userList = getUserList()
            commandArray = userFix(commandString, user)
            print ("DB: ", commandArray)
            data["inputs"] = [commandArray]
            runSys(data)
        print ("done this")
    print ("DONE ALL")

############
# Download #
############
def download(data):
    dlArray = data["inputs"][0]
    print ("DL")
    print (dlArray)
    for download in dlArray:
        print ()
        print ("NEW")
        print ("A: " + download)
        download = download.split("\t")
        URL = download[0].replace("\n", "")
        sourceArray = URL.split("/")
        filename = sourceArray[len(sourceArray) - 1]
        destName = os.path.join(download[1], filename)
        user = download[2]
        print ("B: " + URL)
        print ("C: " + destName)
        print (os.path.dirname(destName))
        systemScript = "mkdir -p " + escapeString(os.path.dirname(destName))
        commandArray = userFix(systemScript, user)
        data["inputs"]=[commandArray]
        runSys(data)

        try:
            urllib.request.urlretrieve(URL, destName)
            mode = "644"
            systemScript = 'chown ' + user + ":" + user + " " + destName
            commandArray = userFix(systemScript, user)
            data["inputs"] = [commandArray]
            runSys(data)
            systemScript = 'chmod ' + mode + " " + destName
            commandArray = userFix(systemScript, user)
            data["inputs"] = [commandArray]
            runSys(data)
        except:
            print ("Couldn't download", URL)

        print ("done this")
    print ("DONE ALL")

###########
# Install #
###########
def install(data):
    programs = data["inputs"][0]
    host = data["inputs"][1]
    for program in programs:
        program = program.replace("\n","")
        commandString = "dpkg -s " + program + " | grep Status"
        if (host != "localhost"):
            commandArray = ["ssh", host, commandString]
        else:
            commandArray = shlex.split(commandString)
        data["inputs"]=[commandArray]
        myOutput = runSys(data)
        if (len(myOutput) == 0):
            commandString = "sudo apt-get -y install " + program
            if (host != "localhost"):
                commandArray = ["ssh", "-t", "-t", host, commandString]
            else:
                commandArray = shlex.split(commandString)
            data["inputs"]=[commandArray]
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

    commandArray = shlex.split(commandString)
    data["inputs"]=[commandArray]
    runSys(data)
    

##############
# Import PPA #
##############
def importPPA(data):
    PPAList = data["inputs"][0].splitlines()
    for PPA in PPAList:
        commandString = "sudo add-apt-repository ppa:" + PPA
        commandArray = shlex.split(commandString)
        data["inputs"]=[commandArray]
        runSys(data)
        
    commandString = "sudo add-get update"
    commandArray = shlex.split(commandString)
    data["inputs"]=[commandArray]
    runSys(data)

##################
# Import GPG Pub #
##################
def importGPGPub(data):
    print ("IMPORT")
    user = data["inputs"][0]
    print ("path is:")
    keyPath = joinFolder(data["inputs"][1])
    print (keyPath)
    commandString = "gpg --import " + keyPath
    commandArray = userFix(commandString, user)
    data["inputs"]=[commandArray]
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

    data["inputs"] = ["f", "false", "false", "false", [inputDir], "localhost", [thisRegex]]

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
    data["inputs"] = ["f", "false", "false", "false", [inputDir], "localhost", [thisRegex]]
    fileArray = getMatchContents(data)
    #yLabels = []
    cStart = 3
    for filePath in fileArray:
        split = filePath.split("/")
        baseFolder = split[len(split)-2]

        dirname = os.path.dirname(filePath)
        confName = joinFolder([tempFolder, dirname, "conf.conf"])
        inputName = joinFolder([tempFolder, filePath])
        outputName = joinFolder([tempFolder, dirname, "OUT" + baseFolder +".csv"])
        cumOutName = joinFolder([tempFolder, dirname, "CUMOUT" + baseFolder +".csv"])
        with open (inputName, "r") as inputFile:

            inputRows = inputFile.readlines()
            with open(confName, 'rb') as confFile:
                confRowsRaw = confFile.readlines()
                confRows =[]
                for row in confRowsRaw:
                    confRows.append(str(row, 'utf-8').replace("\n",""))
                countType = confRows[2]

                with open(outputName, "w") as outputFile:
                    outputRows = [confRows[2]]
                    i = 0
                    j = 0
                    for inputArray in csv.reader(inputRows):
                        if  (i > 0):
                            newValue = ""
                            j = 0
                            toAdd = []
                            for confRow in confRows:
                                if (j > cStart):
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
                                            string = inputArray[int(confArray[k])]
                                            try:
                                                value = float(string)
                                            except:
                                                value = 0
                                            newValue +=  value * float(confArray[k + 1])
                                    toAdd.append(newValue)
                                j = j + 1
                            outputRows.append(toAdd)
                        i += 1
                    sortRows = outputRows[1:]
                    sortRows = sorted(sortRows, key=lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y"))
                    csvRows = []
                    for sortedRow in sortRows:
                        toAdd = ""
                        i = 0
                        for element in sortedRow:
                            if (toAdd == ""):
                                toAdd = str(element)
                            else:
                                toAdd = toAdd + "," + str(element)
                            i += 1
                        csvRows.append(toAdd)
                            
                    csvRows.insert(0, outputRows[0])
                                    
                    for csvRow in csvRows:
                        outputFile.write("%s\n" % csvRow)
                        
                    if (countType == "cumul"):
                        csvRows = []
                        i = 0
                        for sortedRow in sortRows:
                            sortRows[i][1] = float(sortRows[i][1])
                            if (i > 0):
                                sortRows[i][1] = sortRows[i - 1][1] + float(sortRows[i][1])
                            i += 1
                            toAdd = ""
                            j = 0
                            for element in sortedRow:
                                if (toAdd == ""):
                                    toAdd = str(element)
                                else:
                                    toAdd = toAdd + "," + str(element)
                                j += 1
                            csvRows.append(toAdd)
                            
                        csvRows.insert(0, outputRows[0])
                        with open(cumOutName, "w") as cumOutFile:
                            for csvRow in csvRows:
                                cumOutFile.write("%s\n" % csvRow)
                        
    thisRegex = ".meta"
    data["inputs"] = ["f", "false", "false", "false", [inputDir], "localhost", [thisRegex]]
    fileArray = getMatchContents(data)
    for filePath in fileArray:
        print ()
        print()
        print ("FP IS")
        print (filePath)
        inputPath = joinFolder([tempFolder, filePath])
        outPath = joinFolder([tempFolder,filePath.split(".")[0]+"OUT.csv"])
        with open (inputPath, "r") as inputFile:
            with open (outPath, "w") as outputFile:
                outputFile.write("%s\n" % "Date,Total")
                toMerge = inputFile.read().splitlines()
                print ("LIS")
                print (toMerge)
                allRows=[]
                for sourcePath in toMerge:
                    fullSourcePath = joinFolder([tempFolder,sourcePath])
                    print (fullSourcePath)
                    with open(fullSourcePath, "r") as sourceFile:
                        sourceRows = sourceFile.readlines()
                        i = 0
                        for rowArr in csv.reader(sourceRows):
                            if (i > 0):
                                allRows.append(rowArr)
                            i += 1

                print (allRows)
                sortRows = sorted(allRows, key=lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y"))
                csvRows = []
                i = 0
                for sortedRow in sortRows:
                    sortRows[i][1] = float(sortRows[i][1])
                    if (i > 0):
                        sortRows[i][1] = sortRows[i - 1][1] + float(sortRows[i][1])
                    i += 1
                    toAdd = ""
                    j = 0
                    for element in sortedRow:
                        if (toAdd == ""):
                            toAdd = str(element)
                        else:
                            toAdd = toAdd + "," + str(element)
                        j += 1
                    csvRows.append(toAdd)
                            
                for row in csvRows:
                    outputFile.write("%s\n" % row)                
        print ("DONE!")
    thisRegex = "OUT"
    data["inputs"] = ["f", "start", "false", "false", [inputDir], "localhost", [thisRegex]]
    fileArray = getMatchContents(data)

    i = 0
    for filePath in fileArray:
        outputPath = joinFolder([tempFolder, os.path.dirname(filePath), os.path.basename(filePath)[:3] + "graph.png"])
        inputPath = joinFolder([tempFolder, filePath])
        print ("!")
        print (inputPath)
        print (outputPath)
        commandString = "gnuplot -e \"filename='" + inputPath+"'\" -e \"outputpath='" + outputPath+"'\" /home/adam/Projects/mullet/gnuplot.gp"
        #commandArray = ['gnuplot -e \"filename=' + inputPath + '\" -e \"outputpath=' + outputPath + '\" /home/adam/Projects/mullet/gnuplot.gp']
        #print (commandArray)
        #sys.exit()
        #commandArray = ["gnuplot", "-e \"filename='" + inputPath+"'",  "-e \"outputpath='" + outputPath, "/home/adam/Projects/mullet/gnuplot.gp"]
        data["inputs"] = [shlex.split(commandString)]
        #data["inputs"] = [commandArray]
        runSys(data)
        i += 1

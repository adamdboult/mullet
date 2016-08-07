##########
# Import #
##########
import os
import zipfile
import tarfile
import subprocess
import shutil
import re
import subprocess
import json
import sys
import tempfile
import socket

localhost = "localhost"

inputPath = sys.argv[1]
with open(inputPath) as data_file:
    data = json.load(data_file)

tempFolder = tempfile.mkdtemp()

#######################
# Get folder contents #
#######################
def getFolderContents(fileOrFolder, folder, host):
    commandArray = ["ssh", "%s" % host]
    if (host == localhost):
        commandArray=[]
    commandArray.append("find")
    commandArray.append(folder)
    commandArray.append("-type")
    commandArray.append(fileOrFolder)
    ssh = subprocess.Popen(commandArray,
                           shell = False,
                           stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE)

    results = ssh.stdout.read().splitlines()
    resultOutput =[]
    for entry in results:
        newA = str(entry,'utf-8')[len(folder):]
        resultOutput.append(newA)

    return resultOutput

#####################
# Copy file to temp #
#####################
def toTemp(sourceFile, sourceFolder, sourceHost):
    filename, file_extension = os.path.splitext(sourceFile)
    
    sourcePath = os.path.join(sourceFolder, sourceFile)
    tempPath   = os.path.join(tempFolder, sourceFile)
    
    tempString = '"' + tempPath + '"'
    sourceString = sourceHost + ':"' + sourcePath + '"'
    if (sourceHost == localhost):
        sourceString = '"' + sourcePath + '"'

    systemScript = 'rsync -avz --protect-args '+ sourceString + ' ' + tempString

    makeDir = os.path.dirname(tempPath)
    try:
        os.stat(makeDir)
    except:
        os.makedirs(makeDir)
    os.system(systemScript)
    
##################
# Unzip function #
##################
def unZip():
    folderContents = getFolderContents("f", tempFolder, localhost)
    for folderContent in folderContents:
        #filename, file_extension = os.path.splitext(folderContent)
        #if (filename[0]=="/"):
        #    filename = filename[1:]

        filePath = os.path.join(tempFolder, folderContent)
        os.chdir(tempFolder)
        if (filePath.endswith(".zip")):
            print ("Using zip")
            fh = open(filePath, 'rb')
            z = zipfile.ZipFile(fh)
            for name in z.namelist():
                outpath = folderPath
                z.extract(name, outpath)
            fh.close()

        elif (filePath.endswith("tar.gz")):
            print ("Using tar.gz")
            tar =  tarfile.open(filePath, "r:gz")
            tar.extractall()
            tar.close()

        elif (filePath.endswith("tar")):
            print ("Using tar")
            tar =  tarfile.open(filePath, "r:")
            tar.extractall()
            tar.close()

        else:
            print ("Using other")

#################
# Escape string #
#################
#def escapeString(inputString):
#    outputString = inputString.replace(" ", "\ ").replace("(", "\(").replace(")","\)").replace("|", "\|").replace("\n","")
#    return outputString

###############
# Create file #
###############
def newFile(path):
    newPath = os.path.join(tempFolder, path)
    open(newPath, "w").close()

###############
# Expand file #
###############
def expandFile(rawPath, expandPath, writePath):
    rawPath = os.path.join(tempFolder, rawPath)
    expandPath = os.path.join(tempFolder, expandPath)
    writePath = os.path.join(tempFolder, writePath)
    with open (writePath, "w") as outFile:
        with open (rawPath) as rawFile:
            with open (expandPath) as expandFile:
                expandLines = expandFile.read().splitlines()
                for rawLine in rawFile:
                    for expandLine in expandLines:
                        outFile.write(expandLine.replace("\n","") + rawLine)

###############
# Write value #
###############
def writeValue(writePath):
    writePath = os.path.join(tempFolder, writePath)
    with open (writePath, "w") as outFile:
        rawLine = socket.gethostname()
        outFile.write(rawLine)
                        
###############
# Filter file #
###############
def filterFile(rawPath, filterPath, writePath):
    rawPath = os.path.join(tempFolder, rawPath)
    filterPath = os.path.join(tempFolder, filterPath)
    writePath = os.path.join(tempFolder, writePath)
    with open (writePath, "w") as outFile:
        with open (rawPath) as rawFile:
            with open (filterPath) as filterFile:
                filterLines = filterFile.read().splitlines()
                for rawLine in rawFile:
                    write = 1
                    for filterLine in filterLines:
                        if (filterLine.strip() == rawLine.strip()):
                            write = 0
                    if (write == 1):
                        outFile.write(rawLine)

###############
# Append file #
###############
def appendFile(readPath, writePath, skipRow, skipCol):
    readPath = os.path.join(tempFolder, readPath)
    writePath = os.path.join(tempFolder, writePath)
    with open (writePath, "a") as outfile:
        with open (readPath) as infile:
            row = 0
            for line in infile:
                if (row >= skipRow):
                    outfile.write(line[skipCol:])
                row += 1

##################
# Convert to MP3 #
##################
def toMP3(bitrate):
    folderContents = getFolderContents("f", tempFolder, localhost)
    for folderContent in folderContents:
        filename, file_extension = os.path.splitext(folderContent)
        if (filename[0]=="/"):
            filename = filename[1:]

        folderPath = os.path.join(tempPath, filename)
        filePath = os.path.join(folderPath + file_extension)
        destPath = os.path.join(folderPath + ".mp3")
        if (filePath.endswith("flac")):

            systemScript = 'ffmpeg -i ' + filePath + ' -qscale:a 2 ' + destPath
            print (systemScript)
            os.system(systemScript)

#######################
# Copy to destination #
#######################
def toDest(destFolder, destHost, regexArray):
    confLines = data["toDestCriteria"]
    allowedExtensions = data["allowedExtensions"]
    
    tempFiles = getFolderContents("f", tempFolder, localhost)
    matchFileArray = []
    print ("TTT")
    print (tempFiles)
    for tempFile in tempFiles:
        if (tempFile[0]=="/"):
            tempFile = tempFile[1:]

        filename, file_extension = os.path.splitext(tempFile)
        if (
                len(allowedExtensions) == 0 or
                file_extension in allowedExtensions
        ):
            if (len(regexArray) == 0):
                matchFileArray.append(tempFile)
            else:
                thisMatch = 0
                for regex in regexArray:
                    pattern = re.compile(regex)
                    if (pattern.match(tempFile)):
                        thisMatch = 1
                if (thisMatch == 1):
                    matchFileArray.append(tempFile)

    print (matchFileArray)
    for matchFile in matchFileArray:
        filename, file_extension = os.path.splitext(matchFile)

        destPath = os.path.join(destFolder, matchFile)
        destString = '"' + destHost + ':' + destPath + '"'
        if (destHost == localhost):
            destString = '"' + destPath + '"'

        tempString = '"' + os.path.join(tempFolder, matchFile) + '"'

        commandArray = ["ssh", "%s" % destHost]
        if (destHost == localhost):
            commandArray=[]

        commandArray.append("mkdir")
        commandArray.append("-p")
        commandArray.append(os.path.dirname(destPath))
        ssh = subprocess.Popen(commandArray,
                               shell = False,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE)

        results = ssh.stdout.readlines()
        systemScript = 'rsync -avz --protect-args ' + tempString + ' ' + destString
        print (systemScript)
        os.system(systemScript)

# ... do stuff with dirpath
def closeTemp():
    print("by")
    shutil.rmtree(tempFolder)

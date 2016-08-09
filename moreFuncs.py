##########
# Import #
##########
import os
import socket

import zipfile
import tarfile

###############
# Expand file #
###############
def expandFile(data, rawPath, expandPath, writePath):
    tempFolder = data["tempFolder"]
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
def writeValue(data, writePath):
    tempFolder = data["tempFolder"]
    writePath = os.path.join(tempFolder, writePath)
    with open (writePath, "w") as outFile:
        rawLine = socket.gethostname()
        outFile.write(rawLine)
                        
###############
# Filter file #
###############
def filterFile(data, rawPath, filterPath, writePath):
    tempFolder = data["tempFolder"]
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
def appendFile(data, readPath, writePath, skipRow, skipCol):
    tempFolder = data["tempFolder"]
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
def toMP3(data, extension, commandArray):
    tempFolder = data["tempFolder"]
    folderContents = getFolderContents("f", tempFolder, "localhost")
    for folderContent in folderContents:
        filename, file_extension = os.path.splitext(folderContent)
        if (filename[0]=="/"):
            filename = filename[1:]
        if (file_extension == extension):
            
            filePath = os.path.join(tempFolder, folderContent)
            folderPath = os.path.join(tempFolder, filename)

            systemScript = ""
            for command in commandArray:
                if (command[0] == "'" or command[0] == '"'):
                    systemScript += command[1:-1]
                else:
                    systemScript +=globals()[command]
            print (systemScript)
            os.system(systemScript)

##################
# Unzip function #
##################
def unZip(data):
    tempFolder = data["tempFolder"]
    folderContents = getFolderContents("f", tempFolder, "localhost")
    for folderContent in folderContents:
        filePath = os.path.join(tempFolder, folderContent)
        os.chdir(tempFolder)

        
        if (filePath.endswith(".zip")):
            fh = open(filePath, 'rb')
            z = zipfile.ZipFile(fh)
            for name in z.namelist():
                outpath = folderPath
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

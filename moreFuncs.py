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

#inputPath = sys.argv[1]
#with open(inputPath) as data_file:
#    data = json.load(data_file)

tempFolder = tempfile.mkdtemp()

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

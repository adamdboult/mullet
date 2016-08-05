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
    tempPath = os.path.join(tempFolder, filename)

    sourcePath = os.path.join(sourceFolder, sourceFile)

    tempString = os.path.join(tempPath, os.path.basename(sourceFile))
    sourceString = sourceHost + ':"' + sourcePath + '"'
    if (sourceHost == localhost):
        sourceString = '"' + sourcePath + '"'

    systemScript = 'rsync -avz --protect-args '+ sourceString + ' "' + tempString + '"'
    print (systemScript)
    os.makedirs(tempPath, exist_ok=True)
    os.chdir(tempPath)
    os.system(systemScript)
    
##################
# Unzip function #
##################
def unZip(sourceFile):

    filename, file_extension = os.path.splitext(sourceFile)
    
    tempPath = os.path.join(tempFolder, filename)

    folderContents = getFolderContents("f", tempPath, localhost)
    for folderContent in folderContents:
        filename, file_extension = os.path.splitext(folderContent)
        if (filename[0]=="/"):
            filename = filename[1:]

        folderPath = os.path.join(tempPath)
        print ("HERE")
        print (tempPath)
        print (filename)
        print (folderPath)
        print(os.path.basename(folderPath))
        print (file_extension)
        filePath = os.path.join(folderPath, os.path.basename(folderPath) + file_extension)
        os.chdir(tempPath)
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
    print ("zippy")
#################
# Escape string #
#################
#def escapeString(inputString):
#    outputString = inputString.replace(" ", "\ ").replace("(", "\(").replace(")","\)").replace("|", "\|").replace("\n","")
#    return outputString

##################
# Convert to MP3 #
##################
def toMP3(sourceFile):
    print ("tompy3")
    bitRate = data["bitRate"]

    filename, file_extension = os.path.splitext(sourceFile)
    
    tempPath = os.path.join(tempFolder, filename)

    folderContents = getFolderContents("f", tempPath, localhost)
    for folderContent in folderContents:
        filename, file_extension = os.path.splitext(folderContent)
        if (filename[0]=="/"):
            filename = filename[1:]

        folderPath = os.path.join(tempPath, filename)
        print ("AA")
        print (folderPath)
        print (filename)
        print (file_extension)
        print (os.path.basename(folderPath))
        filePath = os.path.join(folderPath + file_extension)
        destPath = os.path.join(folderPath + ".mp3")
        if (filePath.endswith("flac")):
            #commandArray=[]
            #commandArray.append('ffmpeg')
            #commandArray.append('-i')
            #commandArray.append('"' + filePath + '"')
            #commandArray.append('-qscale:a')
            #commandArray.append("2")
            #commandArray.append('"' + destPath + '"')

            systemScript = 'ffmpeg -i ' + filePath + ' -qscale:a 2 ' + destPath
            print (systemScript)
            os.system(systemScript)
            #print (commandArray)
            #ssh = subprocess.Popen(commandArray,
            #               shell = False,
            #               stdout = subprocess.PIPE,
            #               stderr = subprocess.PIPE)
            #results = ssh.stdout.readlines()

#######################
# Copy to destination #
#######################
def toDest(sourceFile, destFolder, destHost):
    confLines = data["toDestCriteria"]
    allowedExtensions = data["allowedExtensions"]

    filename, file_extension = os.path.splitext(sourceFile)
    
    tempPath = os.path.join(tempFolder, filename)
    destPathRoot = os.path.join(destFolder, filename)
    
    tempFiles = getFolderContents("f", tempPath, localhost)
    matchFileArray = []
    for tempFile in tempFiles:
        if (tempFile[0]=="/"):
            tempFile = tempFile[1:]

        filename, file_extension = os.path.splitext(tempFile)
        if file_extension in allowedExtensions:
            if tempFile not in matchFileArray:
                matchFileArray.append(tempFile)
    for matchFile in matchFileArray:
        filename, file_extension = os.path.splitext(matchFile)

        destPath = os.path.join(destPathRoot, matchFile)
        destString = '"' + destHost + ':' + destPath + '"'
        if (destHost == localhost):
            destString = '"' + destPath + '"'

        tempString = '"' + os.path.join(tempPath, matchFile) + '"'

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
    #shutil.rmtree(tempFolder)

##########
# Import #
##########
import os
import re
import subprocess

#######################
# Get folder contents #
#######################
def getFolderContents(fileOrFolder, folder, host):
    commandArray = ["ssh", "%s" % host]
    if (host == "localhost"):
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
def toTemp(data, sourceFile):
    print (data)
    sourceFolder = data["sourceFolder"]
    sourceHost = data["sourceHost"]
    tempFolder = data["tempFolder"]
    filename, file_extension = os.path.splitext(sourceFile)
    
    sourcePath = os.path.join(sourceFolder, sourceFile)
    tempPath   = os.path.join(tempFolder, sourceFile)
    
    tempString = '"' + tempPath + '"'
    sourceString = sourceHost + ':"' + sourcePath + '"'
    if (sourceHost == "localhost"):
        sourceString = '"' + sourcePath + '"'

    systemScript = 'rsync -avz --protect-args '+ sourceString + ' ' + tempString

    makeDir = os.path.dirname(tempPath)
    try:
        os.stat(makeDir)
    except:
        os.makedirs(makeDir)
    os.system(systemScript)
    
#######################
# Copy to destination #
#######################
def toDest(data, regexArray):
    destFolder = data["destFolder"]
    destHost = data["destHost"]
    tempFolder = data["tempFolder"]
    confLines = data["toDestCriteria"]
    allowedExtensions = data["allowedExtensions"]
    
    tempFiles = getFolderContents("f", tempFolder, "localhost")
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
        if (destHost == "localhost"):
            destString = '"' + destPath + '"'

        tempString = '"' + os.path.join(tempFolder, matchFile) + '"'

        commandArray = ["ssh", "%s" % destHost]
        if (destHost == "localhost"):
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

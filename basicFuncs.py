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

#############
# Move file #
#############
def moveFile(sourceFile, hosts, folders):
    destHost = hosts[1]
    fromHost = hosts[0]

    destFold = folders[1]
    fromFold = folders[0]
    
    fromPath = os.path.join(fromFold, sourceFile)
    destPath = os.path.join(destFold, sourceFile)
    
    destString = '"' + destPath + '"'
    fromString = '"' + fromPath + '"'

    if (fromHost != "localhost"):
        fromString = fromHost + ':' + fromString
    if (destHost != "localhost"):
        destString = destHost + ':' + destString

    print ("-----------")
    print (sourceFile)
    makeDir = os.path.dirname(destPath)
    try:
        os.stat(makeDir)
    except:
        os.makedirs(makeDir)

    systemScript = 'rsync -avz --protect-args '+ fromString + ' ' + destString
    print (systemScript)
    os.system(systemScript)
    
#######################
# Copy to destination #
#######################
def toDest(data, regexArray, allowedExtensions):
    tempFolder = data["tempFolder"]
    folders = [tempFolder,data["destFolder"]]
    hosts = ["localhost", data["destHost"]]

    tempFiles = getFolderContents("f", tempFolder, "localhost")
    matchFileArray = []
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
        moveFile(matchFile, hosts, folders)

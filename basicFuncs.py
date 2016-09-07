##########
# Import #
##########
import os
import re
import subprocess
import tempfile
import shutil
import copy

#########
# Print #
#########
def printF(data):
    print (data["inputs"])

#############
# Read file #
#############
def readFile(data):
    print ("READING")
    paths = data["inputs"][0]
    skipRow = data["inputs"][1]
    skipCol = data["inputs"][2]

    readPath = joinFolder(paths)
    
    results = []
    with open (readPath) as infile:
        row = 0
        for line in infile:
            if (row >= skipRow):
                results.append(line[skipCol:])
            row += 1
                    
    return results

###############
# Append file #
###############
def appendFile(data):
    print ("appending")
    lines = data["inputs"][0]
    paths = data["inputs"][1]
    fullPath = joinFolder(paths)
    
    with open (fullPath, "a") as outFile:
        for line in lines:
            outFile.write(line)
    return

########
# Join #
########
def joinFolder(folders):
    filePath = "/"
    for path in folders:
        filePath = os.path.join(filePath, path)
    return filePath
    
###############
# Run command #
###############
def runSys(data):
    print ("runsys")
    commandArray = data["inputs"][0]
    host = "localhost"
    if (len(data["inputs"]) > 1):
        host = data["inputs"][1]
    print (commandArray)
    if (host != "localhost"):
        commandHost = ["ssh", "%s" % host]
        for i in range(len(commandHost)):
            commandArray.insert(i, commandHost[i])
    print (commandArray)
    ssh = subprocess.Popen(commandArray,
                           shell = False,
                           stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE)
    errors = ssh.stderr.read().splitlines()
    print ("errors")
    print (errors)
    result = ssh.stdout.read().splitlines()
    return result

#######################
# Get folder contents #
#######################
def getFolderContents(data):
    print ("get folder cont")
    fileOrFolder = data["inputs"][0]
    paths = data["inputs"][1]
    host = data["inputs"][2]

    filePath = joinFolder(paths)

    commandArray = ["find", filePath, "-type", fileOrFolder]
    
    newData = copy.deepcopy(data)
    newData["inputs"] = [commandArray, host]
    results = runSys(newData)
    resultOutput =[]
    for entry in results:
        newA = str(entry,'utf-8')[len(filePath):]
        if (len(newA) > 0):
            if (newA[0] == "/"):
                newA = newA[1:]
            resultOutput.append(newA)
    return resultOutput

#############
# Move file #
#############
def moveFile(data):
    print ("move file")
    sourceFile = data["inputs"][0]
    hosts = data["inputs"][1]
    folders = data["inputs"][2]
    sudo = data["inputs"][3]

    destHost = hosts[1]
    fromHost = hosts[0]

    destFold = folders[1]
    fromFold = folders[0]

    fromPath = joinFolder([fromFold, sourceFile])
    destPath = joinFolder([destFold, sourceFile])

    destString = '"' + destPath + '"'
    fromString = '"' + fromPath + '"'

    if (fromHost != "localhost"):
        fromString = fromHost + ':' + fromString
    if (destHost != "localhost"):
        destString = destHost + ':' + destString

    makeDir = os.path.dirname(destPath)
    try:
        os.stat(makeDir)
    except:
        os.makedirs(makeDir)

    systemScript = 'rsync -az --protect-args '+ fromString + ' ' + destString
    if (sudo == "true"):
        systemScript = "sudo " + systemScript
    print (systemScript)
    os.system(systemScript)

#######################
# Get contents, regex #
#######################
def getMatchContents(data):
    print ("get match contents")
    fileOrFolder = data["inputs"][0]
    whatMatch = data["inputs"][1]
    anti = data["inputs"][2]
    paths = data["inputs"][3]
    host = data["inputs"][4]
    regexArray = data["inputs"][5]

    newInputs = copy.deepcopy(data)
    newInputs["inputs"]=[fileOrFolder, paths, host]
    tempFiles = getFolderContents(newInputs)
    matchFileArray = []
    for tempFile in tempFiles:
        if (tempFile[0]=="/"):
            tempFile = tempFile[1:]
        filename, file_extension = os.path.splitext(tempFile)
        toMatch = tempFile
        toSend = tempFile
        if (whatMatch == "start"):
            toMatch = filename
        if (whatMatch == "end"):
            toMatch = file_extension
            toSend = filename
        if (len(regexArray) == 0):
            matchFileArray.append(tempFile)
        else:
            thisMatch = 0
            for regex in regexArray:
                regex = "^.*"+regex+"*.$"
                pattern = re.compile(regex)
                if (pattern.match(toMatch)):
                    if (len(regex)>0):
                        thisMatch = 1
            if (anti == "true"):
                thisMatch = 1 - thisMatch
            if (thisMatch == 1):
                matchFileArray.append(tempFile)
            else:
                a=1
    print ("contents are")
    print (matchFileArray)
    return matchFileArray

##############
# tempFolder #
##############
def newTemp(data):
    data["tempFolder"] = tempfile.mkdtemp()
    
def tempRefresh(data):
    print ("REFRESH")
    endTemp(data)
    newTemp(data)
    
def endTemp(data):
    data["tempFolder"] = shutil.rmtree(data["tempFolder"])

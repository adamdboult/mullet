##########
# Import #
##########
import os
import re
import subprocess

import shlex
import tempfile
import shutil
import copy
import pwd

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
    print (readPath)    
    results = []
    with open (readPath) as infile:
        row = 0
        for line in infile:
            if (row >= skipRow):
                results.append(line[skipCol:])
            row += 1
    print ("READ")
    return results

###############
# Escape func #
###############
def escapeFunc(string, specials):
    for special in specials:
        string = string.replace(special, "\\" + special)
    return string
        
#################
# Escape string #
#################
def escapeString(string):
    characters = ["(", ")", "-", " ","&"]
    string = escapeFunc(string, characters)
    return string

################
# Escape regex #
################
def escapeRegex(string):
    characters = ["(", ")"]
    string = escapeFunc(string, characters)

    return string

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
    print (commandArray)
    host = "localhost"
    if (len(data["inputs"]) > 1):
        host = data["inputs"][1]

    commandArrays=[]
    cont = True
    while (cont == True):
        try:
            indMatch = commandArray.index("|")
        except:
            indMatch = False
        if (indMatch):
            commandArrays.append(commandArray[:indMatch])
            commandArray = commandArray[indMatch+1:]
        else:
            cont = False
    commandArrays.append(commandArray)
    
    if (host != "localhost"):
        commandHost = ["ssh", "%s" % host]
        for j in range (len(commandArrays)):
            array = commandArrays[j]
            for i in range(len(commandHost)):
                array.insert(i, commandHost[i])
            commandArrays[j] = array
    proc = []
    processInput = None
    for i in range(len(commandArrays)):
        proc.append(
            subprocess.Popen(
                commandArrays[i],
                shell = False,
                stdout = subprocess.PIPE,
                stdin = subprocess.PIPE,
                #stderr = subprocess.PIPE,
                bufsize = 1,
                universal_newlines = True
            )
        )
        processInput = proc[i].communicate(input = processInput)[0].rstrip()
    print (processInput)
    return processInput
        
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
    results = runSys(newData).splitlines()
    resultOutput =[]
    for entry in results:
        print (entry)
        try:
            newA = str(entry,'utf-8')[len(filePath):]
        except:
            newA = entry[len(filePath):]
        if (len(newA) > 0):
            if (newA[0] == "/"):
                newA = newA[1:]
            resultOutput.append(newA)
    return resultOutput

#################
# Get user list #
#################
def getUserList():
    arr = []
    for p in pwd.getpwall():
        arr.append(p[0])
    return arr

#############
# Move file #
#############
def moveFile(data):
    print ("move file")

    sourceFile = data["inputs"][0]
    hosts = data["inputs"][1]
    folders = data["inputs"][2]


    mode = "755"
    user = "false"
    if (len(data["inputs"]) > 3):
        user = data["inputs"][3]
        if (len(data["inputs"]) > 4):
            mode = data["inputs"][4]

    destHost = hosts[1]
    fromHost = hosts[0]

    destFold = folders[1]
    fromFold = folders[0]

    userList = getUserList()
    
    fromPath = joinFolder([fromFold, sourceFile])
    destPath = joinFolder([destFold, sourceFile])

    destString = '"' + destPath + '"'
    fromString = '"' + fromPath + '"'
    
    if (fromHost != "localhost"):
        fromString = fromHost + ':' + fromString
    if (destHost != "localhost"):
        destString = destHost + ':' + destString

    makeDir = os.path.dirname(destPath)

    systemScript = "mkdir -p " + escapeString(makeDir)
    if (destHost != "localhost"):
        systemScript = "ssh " + destHost + " " + systemScript
    if (user == "root"):
        systemScript = "sudo " + systemScript
    elif (user in userList):
        systemScript = "sudo su - " + user + " -c \"" + systemScript + "\""

    try:
        os.stat(makeDir)
    except:
        commandArray = shlex.split(systemScript)
        data["inputs"]=[commandArray]
        runSys(data)

    systemScript = 'rsync -az --protect-args '+ fromString + ' ' + destString
    if (user == "root"):
        systemScript = "sudo " + systemScript
        commandArray = shlex.split(systemScript)
    elif (user in userList):
        systemScriptPre = "sudo su - " + user + " -c"
        commandArray = shlex.split(systemScriptPre)
        commandArray.append(systemScript)
    else:
        commandArray = shlex.split(systemScript)
    data["inputs"]=[commandArray]
    runSys(data)

    # change owner
    if (user != "false"):
        systemScript = 'chown ' + user + ":" + user + " " + destString
        if (user == "root"):
            systemScript = "sudo " + systemScript
            commandArray = shlex.split(systemScript)
        elif (user in userList):
            systemScriptPre = "sudo su - " + user + " -c"
            commandArray = shlex.split(systemScriptPre)
            commandArray.append(systemScript)
        else:
            commandArray = shlex.split(systemScript)
        data["inputs"]=[commandArray]
        runSys(data)

        systemScript = 'chmod ' + mode + " " + destString
        if (user == "root"):
            systemScript = "sudo " + systemScript
            commandArray = shlex.split(systemScript)
        elif (user in userList):
            systemScriptPre = "sudo su - " + user + " -c"
            commandArray = shlex.split(systemScriptPre)
            commandArray.append(systemScript)
        else:
            commandArray = shlex.split(systemScript)
        data["inputs"]=[commandArray]
        runSys(data)

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
    print (tempFiles)
    for tempFile in tempFiles:
        print (tempFile)
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
                regex = escapeRegex(regex)
                regex = "^.*"+regex+".*$"
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
    return matchFileArray

##############
# tempFolder #
##############
def newTemp(data):
    data["tempFolder"] = tempfile.mkdtemp()

    systemScript = 'chmod 777 ' + data["tempFolder"]
    commandArray = shlex.split(systemScript)
    data["inputs"]=[commandArray]
    runSys(data)
    
def tempRefresh(data):
    print ("REFRESH")
    endTemp(data)
    newTemp(data)
    
def endTemp(data):
    data["tempFolder"] = shutil.rmtree(data["tempFolder"])

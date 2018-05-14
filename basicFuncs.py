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

import getpass

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
        if isinstance(path, list):
            path = joinFolder(path)
        if (len(path) > 0):
            if (path[0] == "/"):
                path = path[1:]
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
        print (commandArrays[i])
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
    return processInput
        
#######################
# Get folder contents #
#######################
def getFolderContents(data):
    print ("get folder cont")
    print (data["inputs"])
    fileOrFolder = data["inputs"][0]
    paths = data["inputs"][1]
    host = data["inputs"][2]

    depth = 0
    if (len(data["inputs"]) > 3):
        depth = int(data["inputs"][3])
    
    filePath = joinFolder(paths)
    types = list(fileOrFolder)
    print (types)
    commandArray = ["find", filePath]
    if (depth > 0):
        commandArray.append("-maxdepth")
        commandArray.append(str(depth))
    for typeChar in types:
        commandArray.append("-type")
        commandArray.append(typeChar)
        commandArray.append("-o")
    commandArray.pop()
    newData = copy.deepcopy(data)
    newData["inputs"] = [commandArray, host]
    results = runSys(newData).splitlines()
    resultOutput =[]
    for entry in results:
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
    
    #tempPath = joinFolder([data["tempFolder"], sourceFile])
    
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
        systemScript = "mkdir -p " + escapeString(makeDir)
        if (destHost != "localhost"):
            systemScript = "ssh " + destHost + " " + systemScript
        commandArray = userFix(systemScript, user)

        data["inputs"]=[commandArray]
        runSys(data)

    #if (destHost == "localhost"):

    #destString = '"' + tempPath + '"'
    systemScript = 'rsync -az --protect-args '+ fromString + ' ' + destString
    commandArray = userFix(systemScript, user)
    data["inputs"] = [commandArray]
    print (4)
    runSys(data)
    print (5)
    #fromString = tempString

    # change owner
    if (user != "false"):
        systemScript = 'chown "' + user + ":" + user + '" "' + destString + '"'
        commandArray = userFix(systemScript, user)
        data["inputs"]=[commandArray]
        runSys(data)
        
        systemScript = 'chmod ' + mode + ' "' + destString + '"'
        commandArray = userFix(systemScript, user)
        data["inputs"]=[commandArray]
        runSys(data)
        
    #else:
    #    systemScript = 'rsync -az --protect-args ' + fromString + ' ' + destString
    #    commandArray = userFix(systemScript, user)
    #    data["inputs"]=[commandArray]
    #    print (9)
    #    runSys(data)

    #print (10)


############
# User fix #
############
def userFix(systemScript, user):
    user = user.replace ("\n","")
    userList = getUserList()
    print (user)
    if (user == "root"):
        systemScript = "sudo " + systemScript
        commandArray = shlex.split(systemScript)
    elif (user == getpass.getuser()):
        commandArray = shlex.split(systemScript)        
    elif (user in userList):
        systemScriptPre = "sudo su - " + user + " -c"
        commandArray = shlex.split(systemScriptPre)
        commandArray.append(systemScript)
    else:
        commandArray = shlex.split(systemScript)

    return commandArray
        
#######################
# Get contents, regex #
#######################
def getMatchContents(data):
    print ("get match contents")
    
    fileOrFolder = data["inputs"][0]
    whatMatch = data["inputs"][1]# "start", "end", anything else is whole string
    anti = data["inputs"][2]# if "true", flips it,only find those not matching
    exact = data["inputs"][3]# if "true", look for only exact string, if not look for this in inside another string
    paths = data["inputs"][4]# 
    host = data["inputs"][5]
    regexArray = data["inputs"][6]
    
    newInputs = copy.deepcopy(data)
    newInputs["inputs"] = [fileOrFolder, paths, host]
    tempFiles = getFolderContents(newInputs)

    matchFileArray = []
    for tempFile in tempFiles:
        if (tempFile[0] == "/"):
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
                reallyMatch = toMatch
                if (whatMatch == "start"):
                    regex = regex.split(".")[0]
                    reallyMatch = toMatch.split(".")[0]
                regex = escapeRegex(regex)
                useRegex = "^.*" + regex + ".*$"
                if (exact == "true"):
                    useRegex = "^" + regex + "$"
                pattern = re.compile(useRegex)
                if (pattern.match(reallyMatch)):
                    if (len(regex) > 0):
                        thisMatch = 1
            if (anti == "true"):
                thisMatch = 1 - thisMatch
            if (thisMatch == 1):
                matchFileArray.append(tempFile)
            else:
                a = 1
    print ("\nRemote")
    for filea in tempFiles:
        print (filea)
    print ("\nLocal")
    for fileb in regexArray:
        print (fileb)
    print ("\nEnd:")
    for filec in matchFileArray:
        print (filec)
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
    a = 1
    print ("REFRESH")
    endTemp(data)
    newTemp(data)
    
def endTemp(data):
    data["tempFolder"] = shutil.rmtree(data["tempFolder"])


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
        if (len(download) > 1):
            URL = download[0].replace("\n", "")
            sourceArray = URL.split("/")
            filename = sourceArray[len(sourceArray) - 1]
            destName = os.path.join(download[1], filename)
            user = download[2]
            systemScript = "mkdir -p " + escapeString(os.path.dirname(destName))
            commandArray = userFix(systemScript, user)
            data["inputs"]=[commandArray]
            runSys(data)
            
            try:
                urllib.request.urlretrieve(URL, destName)
                mode = "644"
            
                systemScript = 'chown "' + user + ':' + user + '" "' + destName + '"'
                commandArray = userFix(systemScript, user)
                data["inputs"] = [commandArray]
                runSys(data)
                systemScript = 'chmod ' + mode + ' "' + destName + '"'
                commandArray = userFix(systemScript, user)
                data["inputs"] = [commandArray]
                runSys(data)
            except:
                print ("Couldn't download", URL)

        print ("done this")
    print ("DONE ALL")



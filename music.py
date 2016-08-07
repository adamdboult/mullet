#!/usr/bin/env python3
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

########
# Conf #
########
#localhost = "localhost"
dir = os.path.dirname(os.path.realpath(__file__))

inputPath = sys.argv[1]
with open(inputPath) as data_file:
    data = json.load(data_file)

sourceHost    = data["sourceHost"]
sourceFolder  = data["sourceFolder"]
destHost      = data["destHost"]
destFolder    = data["destFolder"]
functionArray = data["functionArray"]
toTempLimit   = data["toTempLimit"]
toDestCriteria   = data["toDestCriteria"]

#############
# Functions #
#############
from myFuncs import *

########################
# What to copy to temp #
########################

matchType = data["toTempCriteria"]["typeMatch"]

if (matchType == 0):
    destList = []
else:
    destList = getFolderContents(matchType, destFolder, destHost)

sourceList = getFolderContents("f", sourceFolder, sourceHost)

#####################
# Loop through tree #
#####################
copyArraySub = []
toTempArray = []
for sourceFile in sourceList:
    if (matchType == "d"):
        filename, file_extension = os.path.splitext(sourceFile)
        if (filename in destList):
            continue
    elif (matchType == "f"):
        if (sourceFile in destList):
            continue
        
    copyArraySub.append(sourceFile)
    if (len(copyArraySub) == toTempLimit):
        toTempArray.append(copyArraySub)
        copyArraySub=[]

if (len(copyArraySub) > 0 ):
    toTempArray.append(copyArraySub)

for copyArraySub in toTempArray:
    for sourceFile in copyArraySub:
        print ("Copying: " + sourceFile)
        toTemp(sourceFile, sourceFolder, sourceHost)
        
    for entry in functionArray:
        print ("Process: ", entry["name"])
        functionArgs = []
        for arg in entry["args"]:
            if (isinstance(arg, int)):
                newF = arg
            elif (arg[0] == "'" or arg[0] == '"'):
                newF = arg[1:-1]
            else:
                newF = globals()[arg]
            functionArgs.append(newF)
        globals()[entry["name"]](*functionArgs)

        ## empty temp folder

##########
# Finish #
##########
#closeTemp()
print ("done")

###
# other
###

# to temp, to dest merge
# send filters across

# append and new file merge

# test with an album



# split out myFuncs, basic, packages, import all from one folder



###
# deploy
###

# run command against each line (give command, file to func; can do install)
# also for uninstall
# also for git clone
# copy, set up mod and own

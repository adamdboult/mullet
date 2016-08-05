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
localhost = "localhost"
dir = os.path.dirname(os.path.realpath(__file__))

inputPath = sys.argv[1]
with open(inputPath) as data_file:
    data = json.load(data_file)

sourceHost    = data["sourceHost"]
sourceFolder  = data["sourceFolder"]
destHost      = data["destHost"]
destFolder    = data["destFolder"]
functionArray = data["functionArray"]

#############
# Functions #
#############
from myFuncs import *

#####################
# Loop through tree #
#####################
matchType = data["toTempCriteria"]["typeMatch"]
destList   = getFolderContents(matchType, destFolder, destHost)
sourceList = getFolderContents("f", sourceFolder, sourceHost)
print ("dest list")
#print (destList)
for sourceFile in sourceList:
    #print (sourceFile)
    filename, file_extension = os.path.splitext(sourceFile)
    if (filename in destList):
        continue

    print ("Copying: " + sourceFile)
    toTemp(sourceFile, sourceFolder, sourceHost)

    for entry in functionArray:
        print ("Process: ", entry["name"])
        functionArgs = []
        for arg in entry["args"]:
            functionArgs.append(globals()[arg])
        globals()[entry["name"]](*functionArgs)

closeTemp()
print ("done")

#!/usr/bin/env python3
##########
# Import #
##########
import os
import shutil
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

data["localhost"] = "localhost"

#############
# Functions #
#############
from basicFuncs import *
from moreFuncs import *

########################
# What to copy to temp #
########################

if (data["toTempCriteria"]["typeMatch"] == 0):
    destList = []
else:
    destList = getFolderContents(data["toTempCriteria"]["typeMatch"], data["destFolder"], data["destHost"])

sourceList = getFolderContents("f", data["sourceFolder"], data["sourceHost"])

#####################
# Loop through tree #
#####################
copyArraySub = []
toTempArray = []
for sourceFile in sourceList:
    if (data["toTempCriteria"]["typeMatch"] == "d"):
        filename, file_extension = os.path.splitext(sourceFile)
        if (filename in destList):
            continue
    elif (data["toTempCriteria"]["typeMatch"] == "f"):
        if (sourceFile in destList):
            continue
        
    copyArraySub.append(sourceFile)
    if (len(copyArraySub) == data["toTempLimit"]):
        toTempArray.append(copyArraySub)
        copyArraySub=[]

if (len(copyArraySub) > 0 ):
    toTempArray.append(copyArraySub)

for copyArraySub in toTempArray:
    data["tempFolder"] = tempfile.mkdtemp()
    for sourceFile in copyArraySub:
        print ("Copying: " + sourceFile)
        toTemp(data, sourceFile)
        
    for entry in data["functionArray"]:
        print ("Process: ", entry["name"])
        functionArgs = [data]
        for arg in entry["args"]:
            print ("----------")
            if (type(arg) in [list, int]):
                newF = arg
            elif (arg[0] == "'" or arg[0] == '"'):
                newF = arg[1:-1]
            else:
                newF = globals()[arg]
            functionArgs.append(newF)
        globals()[entry["name"]](*functionArgs)

    shutil.rmtree(data["tempFolder"])

##########
# Finish #
##########
print ("done")


###
# other
###

# test with an album

# copy, set up mod and own
# unzip down with command line
### ownquant
#mergeall quant
#copy all across to temp
#for each .conf, concatenate all files in directory
#for each of the concatenated, extract rows, cols
#call gnuplot
#copy gnuplots across to me
##*** filter deploy
#filter copy, use existing conf but replace whitespace with copies. should work
##*** system depoy
###**** easy
#install
#remove
#copy
#git clone if not exist
###**** other
#authkeys
#knowns hosts
#import gnupg public
#import gnpg private

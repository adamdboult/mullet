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
dir = os.path.dirname(os.path.realpath(__file__))

inputPath = sys.argv[1]
with open(inputPath) as data_file:
    future = json.load(data_file)

#############
# Functions #
#############
from basicFuncs import *
from moreFuncs import *

data = {}
newTemp(data)

#############
# Array fix #
#############
def fixArray(data, inputs):
    tempArr = []
    for input in inputs:
        if isinstance(input, list):
            newInput = fixArray(data, input)
        else:
            try:
                newInput = data[input]
            except:
                newInput = input
        tempArr.append(newInput)
    return tempArr

#################
# Loop function #
#################
def nextF(future):
    thisFunction = future[0]
    data["inputs"] = fixArray(data, thisFunction["inputs"])
    try:
        oldResult = copy.deepcopy(data["result"])
    except:
        oldResult = None
        
    try:
        a = thisFunction["response"]
        responseExist = True
    except:
        responseExist = False
    try:
        a = thisFunction["loop"]
        loopExist = True
    except:
        loopExist = False
    data["result"] = globals()[thisFunction["name"]](data)
    if (responseExist):
        newFuture = copy.deepcopy(thisFunction["response"])
        if (loopExist):
            #data[thisFunction["loop"]] = data["result"]
            loopArray = data["result"]
            #try:
            #    print (1)
            #    #loopArray = data[thisFunction["loop"]]
            #    loopArray = data["result"]
            #except:
            #    print (2)
            #    loopArray = thisFunction["loop"]

            keepData = copy.deepcopy(data["result"])
            for loop in loopArray:
                data["result"] = copy.deepcopy(keepData)
                data[thisFunction["loop"]] = loop
                #data["loop"] = loop
                nextF(newFuture)
        else:
            nextF(newFuture)

        try:
            data["result"] = copy.deepcopy(oldResult)
        except:
            data.pop("result", None)

    if (len(future)> 1):
        nextF(future[1:])

#########
# Start #
#########
thisFunction = future[0]
if ("name" not in future[0]):
    for key in thisFunction:
        data[key] = thisFunction[key]
    nextF(future[1:])
else:
    nextF(future)

#######
# End #
#######
endTemp(data)

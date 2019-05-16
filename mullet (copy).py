#!/usr/bin/env python3
##########
# Import #
##########
import os
import shutil
import json
import sys
import tempfile

import socket

import urllib.request

import zipfile
import tarfile
import shlex
import rarfile
import libarchive

import datetime
from operator import itemgetter

import csv

import re
import subprocess

import shutil
import copy
import pwd

import getpass

########
# Conf #
########
dir = os.path.dirname(os.path.realpath(__file__))

userList = []
for p in pwd.getpwall():
    userList.append(p[0])

########
# Keys #
########
"""
def importGPGPub(data):
    print ("IMPORT")
    user = data["inputs"][0]
    print ("path is:")
    keyPath = joinFolder(data["inputs"][1])
    print (keyPath)
    commandString = "gpg --import " + keyPath
    commandArray = userFix(commandString, user)
    data["inputs"]=[commandArray]
    runSys(data)


    {
	"name": "getFolderContents",
	"inputs": ["d", ["path", "keys"], "localhost", 1],
	"loop": "user",
	"response" :[
	    {
		"name": "getFolderContents",
		"inputs": ["f", ["path", "keys", "user", "gpg/gpgPublic/"], "localhost"],
		"loop": "key",
		"response": [
		    {
			"name": "importGPGPub",
			"inputs": ["user", ["path", "keys", "user", "gpg/gpgPublic/", "key"]]
		    }
		]
	    },
	    {
		"name": "getFolderContents",
		"inputs": ["f", ["path", "keys", "user", "gpg/gpgKeys/"], "localhost"],
		"loop": "key",
		"response": [
		    {
			"name": "importGPGPub",
			"inputs": ["user", ["path", "keys", "user", "gpg/gpgKeys/", "key"]]
		    }
		]
	    },
	    {
		"name": "getFolderContents",
		"inputs": ["f", ["path", "keys", "user", "ssh/knownHosts"], "localhost"],
		"loop": "key",
		"response": [
	            {
			"name": "readFile",
			"inputs": [["path", "keys", "user", "ssh/knownHosts/", "key"], 0, 0],
			"response": [
			    {
				"name": "appendFile",
				"inputs": ["result", ["tempFolder", "known_hosts"]]
			    }
			]
		    }
		]
	    },
	    {
		"name": "moveFile",
		"inputs": ["known_hosts", ["localhost", "localhost"], ["tempFolder", ["/home/", "user", "/.ssh/"]], "user"]
	    },
	    {
		"name": "getFolderContents",
		"inputs": ["f", ["path", "keys", "user", "ssh/authorizedKeys"], "localhost"],
		"loop": "key",
		"response": [
	            {
			"name": "readFile",
			"inputs": [["path", "keys", "user", "ssh/authorizedKeys/","key"], 0, 0],
			"response": [
			    {
				"name":"appendFile",
				"inputs": ["result", ["tempFolder", "authorized_keys"]]
			    }
			]
		    }
		]
	    },
	    {
		"name": "moveFile",
		"inputs": ["authorized_keys", ["localhost", "localhost"], ["tempFolder", ["/home/", "user", "/.ssh/"]], "user"]
	    }
	]
    }
"""

mulletInputPath = "/home/adam/ownCloud/PC/mullet/laptop"

###########
# Install #
###########
installPath = os.path.join(mulletInputPath, "install.txt")

with open(installPath) as infile:
    for program in infile:
        print ()

        program = program.replace("\n","")
        if len(program) > 0:
            print (program)
            commandString = "dpkg -s " + program + " | grep \"Status: install\""
            #print (commandString)
            #commandArray = shlex.split(commandString)
            try:
                result = subprocess.check_output(commandString, shell=True, stderr=subprocess.STDOUT).decode("utf-8").replace("\n","")
            except subprocess.CalledProcessError as e:
                result = ""
            #print (result)
            #print (type(result))
            #target = "b'Status: install ok installed\n'"
            #print (target)
            if result != "Status: install ok installed":
                print ("Need to install...")
                commandString = "sudo apt-get -y install " + program
                print (commandString)
                os.system(commandString)

            else:
                print ("Already installed")
            #if result != "Status: install okn


#######
# Git #
#######
print()
gitPath = os.path.join(mulletInputPath, "git.txt")

with open(gitPath) as infile:
    for row in infile:

        row = row.replace("\n","")
        row = row.split("\t")

        if len(row) > 1:

            URL = row[0]
            path = row[1]
            user = row[2]

            URL = URL.replace("\n", "")
            path = path.replace("\n", "")
            user = user.replace ("\n", "")

            filename = URL.split("/")[len(URL.split("/")) - 1].split(".")[0]
            destName = os.path.join(path, filename)

            systemScript = "git clone " + URL + " " + destName


            #print (destName)
            if os.path.isdir(destName) == False:
                print ("Need to clone")
                print (systemScript)
                os.system(systemScript)

                """
                if (user == "root"):
                systemScript = "sudo " + systemScript
                elif (user == getpass.getuser()):
                
                elif (user in userList):
                systemScriptPre = "sudo su - " + user + " -c " + systemScript
                commandArray.append(commandString)
                else:
                commandArray = shlex.split(systemScript)
                """
            else:
                print (filename + " already exists")

############
# Download #
############
print()
downloadPath = os.path.join(mulletInputPath, "download.txt")

with open(downloadPath) as infile:
    for row in infile:

        row = row.replace("\n","")
        row = row.split("\t")

        if len(row) > 1:

            URL = row[0]
            path = row[1]
            user = row[2]

            URL = URL.replace("\n", "")
            path = path.replace("\n", "")
            user = user.replace ("\n", "")

            filename = URL.split("/")[len(URL.split("/")) - 1]
            destName = os.path.join(path, filename)

            systemScript = "wget " + URL + " " + destName

            #print (destName)
            print ()
            if os.path.exists(destName) == False:
                print ("Need to download")
                print (systemScript)
                #os.system(systemScript)

                """
                if (user == "root"):
                systemScript = "sudo " + systemScript
                elif (user == getpass.getuser()):
                
                elif (user in userList):
                systemScriptPre = "sudo su - " + user + " -c " + systemScript
                commandArray.append(commandString)
                else:
                commandArray = shlex.split(systemScript)
                """
            else:
                print (filename + " already exists")


"""
    {
	"name": "readFile",
	"inputs": [["path", "download.txt"], 0, 0],
	"response": [
	    {
		"name": "download",
		"inputs": ["result"]
	    }
	]
    },
"""
##############
# Copy files #
##############
"""
    {
	"name": "getFolderContents",
	"inputs": ["d", ["path", "copy"], "localhost", 1],
	"loop": "user",
	"response": [
	    {
		"name": "getFolderContents",
		"inputs": ["d", ["path", "copy", "user"], "localhost", 1],
		"loop": "code",
		"response": [
		    {
			"name": "getFolderContents",
			"inputs": ["f", ["path", "copy", "user", "code"], "localhost"],
			"loop": "file",
			"response": [
			    {
				"name": "moveFile",
				"inputs": ["file", ["localhost", "localhost"], [["path", "copy", "user", "code"], "/"], "user", "code"]
			    }
			]
		    }
		]
	    }
	]
    }
"""


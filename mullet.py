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

mulletInputPath = "/home/adam/ownCloud/PC/mullet/laptop"
    
########
# Keys #
########
keyPath = os.path.join(mulletInputPath, "keys")
keyUsers = os.listdir(keyPath)
for keyUser in keyUsers:
    print ()
    print (keyUser)

    ###
    # GPG keys
    ###
    print ("Importing GPG keys")
    gpgKeyPath = os.path.join(keyPath, keyUser, "gpg", "gpgKeys")
    gpgKeys = os.listdir(gpgKeyPath)

    for gpgKey in gpgKeys:
        gpgKeyFile = os.path.join(gpgKeyPath, gpgKey)

        commandString = "gpg --import " + gpgKeyFile
        print (commandString)
        os.system(commandString)

    ###
    # GPG Public keys
    ###
    print ("Importing GPG public keys")
    gpgPublicPath = os.path.join(keyPath, keyUser, "gpg", "gpgPublic")
    gpgPublicKeys = os.listdir(gpgPublicPath)

    for gpgPublicKey in gpgPublicKeys:
        gpgPublicKeyFile = os.path.join(gpgPublicPath, gpgPublicKey)
        commandString = "gpg --import " + gpgPublicKeyFile
        os.system(commandString)
        print (commandString)

    ###
    # Authorised keys
    ###
    print ("Importing authorised keys")
    
    authorisedKeysPath = os.path.join(keyPath, keyUser, "ssh", "authorizedKeys")
    authorisedKeys = os.listdir(authorisedKeysPath)
    
    j = 0

    for authorisedKey in authorisedKeys:
        if j == 0:
            commandString = "rm /home/" + keyUser + "/.ssh/authorized_keys"
            os.system(commandString)
            print (commandString)

        authorisedKeyFile = os.path.join(authorisedKeysPath, authorisedKey)
        destPath = os.path.join("/", "home", keyUser, ".ssh", "authorized_keys")
        commandString = "cat " + authorisedKeyFile + " >> " + destPath
        os.system(commandString)
        print (commandString)

        j = 1

    ###
    # Known hosts
    ###
    print ("Importing known hosts")
    
    knownHostPath = os.path.join(keyPath, keyUser, "ssh", "knownHosts")
    knownHosts = os.listdir(knownHostPath)

    j = 0
    for knownHost in knownHosts:
        if j == 0:
            commandString = "rm /home/" + keyUser + "/.ssh/known_hosts"
            os.system(commandString)
            print (commandString)

        knownHostFile = os.path.join(knownHostPath, knownHost)
        destPath = os.path.join("/", "home", keyUser, ".ssh", "known_hosts")
        commandString = "cat " + knownHostFile + " >> " + destPath
        os.system(commandString)
        print (commandString)

        j = 1

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
            print(destName)
            systemScript = "git clone " + URL + " '" + destName + "'"
            print (systemScript)


            #print (destName)
            if os.path.isdir(destName) == False:
                print ("Need to clone")

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

            systemScript = "wget " + URL + " -O " + destName

            #print (destName)
            print ()
            if os.path.exists(destName) == False:
                print ("Need to download")
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
                print (filename + " already exists in " + path)

##############
# Copy files #
##############
print()
print ("Copying")
copyPath = os.path.join(mulletInputPath, "copy")

copyUsers = os.listdir(copyPath)

for copyUser in copyUsers:
    #print(copyUser)
    copyUserPath = os.path.join(copyPath, copyUser)
    copyPermissions = os.listdir(copyUserPath)
    for copyPermission in copyPermissions:
        print ()
        print (copyUser + ", " + copyPermission)
        copyPermissionPath = os.path.join(copyUserPath, copyPermission)
        for (dirpath, dirnames, filenames) in os.walk(copyPermissionPath):
            #print (dirnames)
            for f in filenames:
                sourcePath = os.path.join(dirpath, f)
                destPath = os.path.join(dirpath.replace(copyPermissionPath, ""), f)
                if os.path.exists(destPath) == False:
                    commandString = "cp '" + sourcePath + "' '" + destPath + "'"
                    print (commandString)
                    os.system(commandString)

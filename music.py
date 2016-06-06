#########
# To do #
#########

################
# Dependencies #
################
#ffmpeg

##########
# Import #
##########
import os
import zipfile
import tarfile
import subprocess


########
# Conf #
########
from myConf import *

dir = os.path.dirname(__file__)
recordFile = os.path.join(dir, 'musicRecord.txt')
##########################
# Get list of done files #
##########################
musicList = []
with open(recordFile) as pathFile:
    listTest = pathFile.readlines()
    for listObj in listTest:
        musicList.append(listObj.replace('\n',''))

##################
# Unzip function #
##################
def unzipMusic(fileObj, prePathLocal):
    filename, file_extension = os.path.splitext(fileObj)
    folderPath = os.path.dirname(prePathLocal + filename + "/")
    filePath = folderPath + "/" + os.path.basename(folderPath) + file_extension
    os.chdir(folderPath)
    if (filePath.endswith(".zip")):
        print ("Using zip")
        fh = open(filePath, 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            outpath = folderPath
            z.extract(name, outpath)
        fh.close()

    elif (filePath.endswith("tar.gz")):
        print ("Using tar.gz")
        tar =  tarfile.open(filePath, "r:gz")
        tar.extractall()
        tar.close()

    elif (filePath.endswith("tar")):
        print ("Using tar")
        tar =  tarfile.open(filePath, "r:")
        tar.extractall()
        tar.close()

    else:
        print ("Using other")

########################
# Ensure folders exist #
########################
def folderCheck(prePathLocal, fileObj):
    filename, file_extension = os.path.splitext(fileObj)
    folderPath = os.path.dirname(prePathLocal + filename + "/")
    ### Local folders
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

#############
# Copy file #
#############
def copyFile(fileObj, prePathLocal):
    filename, file_extension = os.path.splitext(fileObj)
    folderPath = os.path.dirname(prePathLocal + filename + "/")
    filePath = folderPath + "/" + os.path.basename(folderPath) + file_extension
    os.chdir(folderPath)
    remotePath = sourceFolder + filePath
    remotePath = remotePath.replace(" ", "\ ").replace("(", "\(").replace(")","\)").replace("|", "\|")
    filePath=filePath.replace(" ", "\ ").replace("(", "\(").replace(")","\)").replace("|", "\|")
    systemScript = 'rsync -avz '+HOST+'":'+remotePath + '" ' + filePath
    print (systemScript)
    #os.system(systemScript)

##################
# Convert to MP3 #
##################
def toMP3(fileObj, prePathLocal, bitRate):
    filename, file_extension = os.path.splitext(fileObj)
    folderPath = os.path.dirname(prePathLocal + filename + "/")
    filePath = folderPath + "/" + os.path.basename(folderPath) + file_extension
    os.chdir(folderPath)
    print ("IN: "+folderPath)
    toMp3Path = os.path.join(dir, 'tomp3.sh')
    subprocess.call(toMp3Path)
    systemScript = 'find . -name "*.flac" -type f -delete; find . -name "*.gz" -type f -delete; find . -name "*.zip" -type f -delete; find . -name "*.tar" -type f -delete'
    os.system(systemScript)
    
    systemScript = 'mv ' + prePathLocal + '**/* ' + destinationFolder
    os.system(systemScript)

##############
# Update log #
##############
def updateLog(recordFile, fileObj):
    with open(recordFile, "a") as myfile:
        myfile.write(fileObj + "\n")

#####################
# Flatten directory #
#####################
def flattenDir(fileObj, prePathLocal):
    filename, file_extension = os.path.splitext(fileObj)
    folderPath = os.path.dirname(prePathLocal + filename + "/")
    filePath = folderPath + "/" + os.path.basename(folderPath) + file_extension
    systemScript = 'find ./ -mindepth 2 -type f -exec mv -i "{}" ./ ";"'#;find -mindepth 1 -maxdepth 1 -type d -exec rm -r {} \;'
    os.chdir(folderPath)
    os.system(systemScript)
    systemScript = 'rm -r */'
    os.chdir(folderPath)
    print ("Running: " + systemScript)
    os.system(systemScript)
    
#############
# Call tree #
#############
COMMAND = "cd " + sourceFolder + "; find . -type f"
ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

fileListPre = ssh.stdout.readlines()
fileList = []
for fileEntry in fileListPre:
    fileList.append(fileEntry.replace('\n','')[2:])

#####################
# Loop through tree #
#####################
i = 0
bitRate = 256
for fileObj in fileList:
    if (fileObj in musicList):
        continue

    print ("Starting: " + fileObj)
    
    print ("Folder Check")
    folderCheck(prePathLocal, fileObj)

    print ("Copy file")
    copyFile(fileObj, prePathLocal)

    print ("Unzip file")
    unzipMusic(fileObj, prePathLocal)

    print ("Flatten directory")
    flattenDir(fileObj, prePathLocal)
    
    print ("Convert files")
    toMP3(fileObj, prePathLocal, bitRate)

    updateLog(recordFile, fileObj)
    print ("Done")

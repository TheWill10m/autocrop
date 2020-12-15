import subprocess
import re
import time

workingDir = ""

currentFiles = []
oldFiles = []
newFiles = []
removedFiles = []
queue = []

def getCurrentFiles():
    out = subprocess.Popen(['ls', workingDir + 'Input/'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)

    stdout,stderr = out.communicate()

    files = stdout.decode("utf-8")
    currentFiles = files.split("\n")[:-1]
    #print("Input contains: ", currentFiles)
    return currentFiles

def getOldFiles():
    log = open(workingDir + 'log.txt', 'r')
    files = log.readlines()
    log.close()

    for i in range(len(files)):
        files[i] = files[i][:-1]

    return files

def writeCurrentFiles(files):
    log=open(workingDir + 'log.txt','w')
    for file in files:
        log.write(file + "\n")
    log.close()

def getNewFiles(currentFiles, oldFiles):
    files = []
    for currentFile in currentFiles:
        if currentFile not in oldFiles:
            files.append(currentFile)
    
    #print("New files: \n", files)
    return files

def getRemovedFiles(currentFiles, oldFiles):
    files = []
    for file in oldFiles:
        if file not in currentFiles:
            files.append(file)
    
    print("Removed files: \n", files)
    return files

def getFileSize(file):
    subprocess.call([workingDir + 'size.sh', workingDir + "Input/" + file, workingDir])
    sizeFile = open(workingDir + 'size.txt','r')
    line = sizeFile.read()
    sizeFile.close()
    subprocess.call(['rm', workingDir + 'size.txt'])

    if "Device or resource busy" in line:
        return False
    else:
        return True

def transcode(files):
    notTranscoded = []
    for file in files:
        if getFileSize(file):
            crop = getCrop(file)
            subprocess.call([workingDir + 'crop.sh', workingDir + 'Input/' + file, crop,
            workingDir + 'Output/' + file, workingDir + 'Processed/' + file])
        else:
            notTranscoded.append(file)
    return notTranscoded

def getCrop(file):
    subprocess.call([workingDir + 'cropdetect.sh', workingDir + "Input/" + file, workingDir])
    cropdetect=open(workingDir + 'crop.txt','r')
    crop = cropdetect.read()
    cropdetect.close()
    subprocess.call(['rm', workingDir + 'crop.txt'])
    return crop

currentFiles = getCurrentFiles()
oldFiles = getOldFiles()
newFiles = getNewFiles(currentFiles, oldFiles)


print("New files detected\n", newFiles)
failed = transcode(newFiles)

for file in failed:
    currentFiles.remove(file)
writeCurrentFiles(currentFiles)
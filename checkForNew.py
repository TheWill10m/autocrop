import subprocess

currentFiles = []
oldFiles = []
newFiles = []
removedFiles = []
queue = []

def getCurrentFiles():
    out = subprocess.Popen(['ls', 'Input/'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)

    stdout,stderr = out.communicate()

    files = stdout.decode("utf-8")
    currentFiles = files.split("\n")[:-1]
    #print("Input contains: ", currentFiles)
    return currentFiles

def getOldFiles():
    log = open('log.txt', 'r')
    files = log.readlines()
    log.close()

    for i in range(len(files)):
        files[i] = files[i][:-1]

    return files

def writeCurrentFiles(files):
    log=open('log.txt','w')
    for file in files:
        log.write(file + "\n")
    log.close()

def getNewFiles(currentFiles, oldFiles):
    files = []
    for currentFile in currentFiles:
        if currentFile not in oldFiles:
            files.append(currentFile)
    
    print("New files: \n", files)
    return files

def getRemovedFiles(currentFiles, oldFiles):
    files = []
    for file in oldFiles:
        if file not in currentFiles:
            files.append(file)
    
    print("Removed files: \n", files)
    return files

def transcode(file):
    crop = getCrop(file)
    subprocess.call(['./crop.sh', file, crop])

def getCrop(file):
    subprocess.call(['./cropdetect.sh', file])
    cropdetect=open('crop.txt','r')
    crop = cropdetect.read()
    cropdetect.close()
    return crop

def getQueue():
    queue = []
    qFile=open('queue.txt','r')
    queue = qFile.readlines()
    qFile.close()

    for i in range(len(queue) - 1):
        queue[i] = queue[i][:-1]
    return queue

def writeQueue(queue):
    file = open('queue.txt', 'w')
    for item in queue:
        file.write(item + "\n")
    file.close()

def addToQueue(files, queue):
    for file in files:
        queue.append(file)

def checkTranscoding():
    file=open("transcoding.txt")
    transcoding = file.readline()
    file.close()

    if transcoding[:-1] == "True":
        return True
    else:
        return False

currentFiles = getCurrentFiles()
oldFiles = getOldFiles()
newFiles = getNewFiles(currentFiles, oldFiles)
writeCurrentFiles(currentFiles)

print("Current files:\n", currentFiles)

queue = getQueue()
addToQueue(newFiles, queue)

print("Queue:\n", queue)

if not checkTranscoding() and len(queue) > 0:
    print("Going to transcode ", queue[0])
    transcode(queue.pop(0))

writeQueue(queue)
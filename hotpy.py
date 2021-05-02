#!/usr/bin/python3.8

#A autoloader for python scripts created by Ben Herbst
#Use python3 hotpy.py [main script name] [optional directory] [optional sleep time in milisecounds]

import time
import subprocess
import sys
import os

dir = ""
dead = False


#Get all files of directory
def getFiles():
    filenames = []
    for path, subdirs, files in os.walk(dir):
        for name in files:
            #Set filter to .py .kv .glade, files like .png give a unicode error
            if name.endswith(('.py', '.kv', '.glade')):
                filenames.append(os.path.join(path, name))

    return filenames


#Get the text of a array of filepaths in a array
def getDataOfFiles(filenames):
    dataOfFiles = []
    for file in filenames:
        dataOfFiles.append(open(file, "r").read())
    return dataOfFiles


if __name__ == "__main__":
    if len(sys.argv) > 2:
        dir = sys.argv[2]
    #Get all files
    before_files = getFiles()
    #Get text of all files
    before_data = getDataOfFiles(before_files)
    #Get main script via first arg
    script = ""
    if len(sys.argv) > 1:
        if dir != "":
            script = dir + "/" + sys.argv[1]
        else:
            script = sys.argv[1]
    else:
        print("No main script argument, use python3 hotpy.py [main script name]")
        exit()
    #Get the sleep time of 3 arg
    if len(sys.argv) > 3:
        sleep = int(sys.argv[3])
    else:
        sleep = 100
    print("<-- Watching " + script + " -->\n")
    print("<-- Start -->\n")
    #Start the main script
    pid = subprocess.Popen([sys.executable, script])

    while True:
        #Look if main script runs
        poll = pid.poll()
        if poll is not None and dead is False:
            print("<-- End -->\n")
            dead = True
        #Get the files and the files text another time, to look for changes
        after_files = getFiles()
        after_data = getDataOfFiles(after_files)
        if after_files != before_files:
            if dead is True:
                dead = False
                print("<-- End -->\n")
            pid.kill()
            print("<-- Start -->\n")
            pid = subprocess.Popen([sys.executable, script])
        if after_data != before_data:
            if dead is True:
                dead = False
                print("<-- End -->\n")
            pid.kill()
            print("<-- Start -->\n")
            pid = subprocess.Popen([sys.executable, script])
        time.sleep(sleep/1000)
        before_files = after_files
        before_data = after_data

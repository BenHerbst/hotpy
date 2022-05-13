#!/usr/bin/python3.8

# a auto reloader for python scripts created by Ben Herbst
# to use it write the following into a terminal: python3 hotpy.py [main script name] [optional directory] [optional sleep time in milisecounds]

import time
import subprocess
import sys
import os

dir = ""
dead = False


# get all files of directory
def getFiles():
    filenames = []
    for path, subdirs, files in os.walk(dir):
        for name in files:
            # set filter to .py .kv .glade, files like .png give a unicode error
            if name.endswith(('.py', '.kv', '.glade')):
                filenames.append(os.path.join(path, name))

    return filenames


# get the text of a array of filepaths in a array
def getDataOfFiles(filenames):
    dataOfFiles = []
    for file in filenames:
        dataOfFiles.append(open(file, "r").read())
    return dataOfFiles


if __name__ == "__main__":
    if len(sys.argv) > 2:
        dir = sys.argv[2]
    # get all files
    before_files = getFiles()
    # get text of all files
    before_data = getDataOfFiles(before_files)
    # get main script via first argument
    script = ""
    if len(sys.argv) > 1:
        script = sys.argv[1]
    else:
        print("No main script argument, use python3 hotpy.py [main script name]")
        exit()
    # get the sleep time of 3th argument if given
    if len(sys.argv) > 3:
        sleep = int(sys.argv[3])
    else:
        # use default sleep time
        sleep = 100
    print("<-- Watching " + script + " -->\n")
    print("<-- Start -->\n")
    # start the main script
    pid = subprocess.Popen([sys.executable, script])

    while True:
        # look if main script runs
        poll = pid.poll()
        if poll is not None and dead is False:
            print("<-- End -->\n")
            dead = True
        # get the files and the files text another time, to look for changes
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

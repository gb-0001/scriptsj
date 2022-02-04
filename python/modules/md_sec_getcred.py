#!/usr/bin/python3
#GB-0001 github

#read basic file 1st line login;password only 2nd line
def mdgetcred(pathfile):
    with open(readfile,'r') as myFile:
        #take line 2
        for i in range(2):
            line = myFile.readline()
        login1,passwd1 = line2.split(";")
    login1 = login1.rstrip('\n')
    passwd1 = passwd1.rstrip('\n')

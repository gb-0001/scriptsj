#!/usr/bin/python

import subprocess
from modules import md_auth_keyring
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-l", "--list", required=True, type=str,
help="path list user password split by ; ")
args = vars(ap.parse_args())


#put dictionnary applist OS user password file src appname;user;password
dicdatuserlist = {}
userlist = open(args["list"], "r")
lines = userlist.readlines()
userlist.close()
for line in lines:
    line = line.strip()
    application,user,password,type1 = line.split(";")
    password = password.strip('\n')
    dicdatuserlist.update({application: (user,password)})


#create credentials keyring
for app1,val1 in dicdatuserlist.items():
    cmd1= 'createcredentials.py -s ' +app1+ ' -u ' +dicdatuserlist[app1][0]+ ' -p ' +dicdatuserlist[app1][1]+ ''
    cmd1tmp = subprocess.Popen(cmd1,shell=True, stdout=subprocess.PIPE)
    (cmd1output, cmd1outputerr) = cmd1tmp.communicate()


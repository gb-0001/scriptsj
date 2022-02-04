#!/usr/bin/python3
##GB-0001 github

from modules import md_passcmd_withkeyring_or_getcred
import argparse
import md_sec_keyring
import md_sec_getcred
import pathlib

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--remoteip", required=True, type=str,
help="Remote IP")
ap.add_argument("-c", "--mycmd", required=True, type=str,
help="remote command to run")
#ap.add_argument("-p", "--passwordmode", required=True,
ap.add_argument("-k", "--myaliaskeyring", required=False, type=str,
help="Define alias keyring ")
ap.add_argument("-f", "--mypathfile", required=False, type=str,
help="Define path file 1st line contain login;password 2nd line your real login;password ")
args = vars(ap.parse_args())

if args["myaliaskeyring"]:
    md_passcmd_withkeyring_or_getcred.sshconnect_remotecmdexec(args["remoteip"],args["mycmd"],args["myaliaskeyring"])
elif args["mypathfile"]:
    file1 = pathlib.Path(args["mypathfile"]):
    if file1.exist():
        user1,password1=md_sec_getcred.mdgetcred(args["mypathfile"])
        md_passcmd_withkeyring_or_getcred.sshconnect_and_passcmd_idpwd(args["remoteip"],args["mycmd"],user1,password1)


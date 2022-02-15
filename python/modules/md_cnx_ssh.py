#!/usr/bin/python3
#GB-0001 github

import os
import sys
import subprocess

import paramiko


# Prerequisite to have done the key exchange beforehand for user
#ex. mdsshcmd(servername,"user","/home/user/.ssh/id_rsa.pub","hostname")
def mdsshcmd(hostname,user,pubkeypath,cmdtopass):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=user,key_filename=pubkeypath)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmdtopass)
#    print("out",ssh_stdout.read())
#    print("IN",ssh_stdin.read())
#    print("ERR",ssh_stderr.read())
    returnvalue=ssh_stdout.read()
    print(ssh_stdin, ssh_stdout, ssh_stderr)
    ssh.close()
    return returnvalue

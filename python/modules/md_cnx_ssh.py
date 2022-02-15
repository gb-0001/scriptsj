#!/usr/bin/python3
#GB-0001 github

import os
import sys
import subprocess

import paramiko




# Prerequisite to have done the key exchange beforehand for user
# example if the key does not exist in the target ~/.ssh/id_rsa 
# ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa 2>/dev/null <<< y >/dev/null
# if the key does exist in the target ~/.ssh/id_rsa    ==>DO
# /usr/bin/sshpass -p "PASSWORD" ssh-copy-id -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa.pub root@IPCENTRALSOURCE
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

def mdssholdcmd(hostname,user,passwd1,cmdtopass):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=user,password=passwd1)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmdtopass)
#    print("out",ssh_stdout.read())
#    print("IN",ssh_stdin.read())
#    print("ERR",ssh_stderr.read())
    returnvalue=ssh_stdout.read()
    print(ssh_stdin, ssh_stdout, ssh_stderr)
    ssh.close()
    return returnvalue

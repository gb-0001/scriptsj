#!/usr/bin/python
##GB-0001 github

import sys
import subprocess
import paramiko
import time
import md_sec_keyring
#import md_sec_getcred

def sshconnect_and_passcmd_idpwd(remoteIp,execCmd,myuser,mypwd):
    sshCli = paramiko.SSHClient()
    sshCli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshCli.connect(hostname=remoteIp,username=myuser,password=mypwd)
    print "Successfully connected to", remoteIp
    remote_connection = sshCli.invoke_shell()
    remote_connection.send(execCmd + "\n")
    time.sleep(1)
    output = remote_connection.recv(65535)
    print output
    remote_connection.send("exit\n")
    sshCli.close

def sshconnect_remotecmdexec(remoteIp,execCmd,myCredential):
    id1,pwd1= mdkeyring(myCredential)
    sshCli = paramiko.SSHClient()
    sshCli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshCli.connect(hostname=remoteIp,username=id1,password=pwd1)
    print "Successfully connected to", remoteIp
    remote_connection = sshCli.invoke_shell()
    remote_connection.send(execCmd + "\n")
    time.sleep(1)
    output = remote_connection.recv(65535)
    print output
    remote_connection.send("exit\n")
    sshCli.close



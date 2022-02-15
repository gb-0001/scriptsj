#!/usr/bin/python3
#GB-0001 github

import subprocess
from sys import platform

#Get short hostname by ip
def mdGetHostnameByIp(myIP):
    ip1 = myIP
    cmdFqdn = subprocess.Popen(['nslookup',ip1], stdout=subprocess.PIPE)
    cmdFqdnOutput = cmdFqdn.stdout.readlines()

    for i in cmdFqdnOutput:
        i= i.strip()
        if "name = " in i:
            break
        else:
           next
    description,fqdn = i.split("name = ")
    hostnameVal = fqdn.split(".")
    return hostnameVal[0]
#example result = mdGetHostnameByIp("192.168.1.1")

#Get fqdn by ip
def mdGetFqdnByIp(myIP):
    ip = myIP
    cmdFqdn = subprocess.Popen(['nslookup',ip], stdout=subprocess.PIPE)
    cmdFqdnOutput = cmdFqdn.stdout.readlines()
    
    for i in cmdFqdnOutput:
        i= i.strip()
        if "name = " in i:
            break
        else:
           next
    description,fqdn = i.split("name = ")

    #start indice -1
    fqdn = fqdn[:-1]
    return fqdn
#example result = mdGetFqdnByIp("192.168.1.1")

#get IP by short hostname
def mdGetIpByHostname(myHOSTNAME):
    hostnameA = myHOSTNAME
    cmdIp = subprocess.Popen(['nslookup',hostnameA], stdout=subprocess.PIPE)
    cmdIpOutput = cmdIp.stdout.readlines()
    cpt=0
    if platform == "linux" or platform =="linux32":
        for i in cmdIpOutput:
            i= i.decode().strip()
            if "#" not in i and i.startswith('Address:'):
                break
        description,ipA = i.split(" ")
        return ipA
    elif platform == "win32"
           for i in cmdIpOutput:
            i= i.decode().strip()
            if i.startswith('Address:'):
                cpt+=1
                if "#" not in i and i.startswith('Address:') and cpt == 2:
                    break
        ipA = i.split(" ")
        return ipA[2]     
#example result = mdGetIpByHostname(monHOSTNAME)


#!/usr/bin/python3

import subprocess
import argparse
from pykeepass import PyKeePass

#pip3 install pykeepass
#createkeyring_with_pykeepass.py -l keepassdb.kdbx -p 'PASSWORD' -g GROUPEKEEPASSFOLDER

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--list", required=True, type=str,
help="path list keepass user password keepassdb.kdbx")
ap.add_argument("-p", "--password", required=True, type=str,
help="define BDD keepass password")
ap.add_argument("-g", "--grpentry", required=True, type=str,
help="Definegroupe example SQLLST")
args = vars(ap.parse_args())

#load BDD keepass
KeepassDB= PyKeePass(args["list"], password=args["password"])

# find groupename
KeepassDBgroup = KeepassDB.find_groups(name='SQLST', first=True)

#Get groupe entry
grplst=KeepassDBgroup.entries
#print("Grouplst:", grplst)

#  dictionnary entry group champ keepass notes wait cpt1/cpt2/appA
dic_alias={}
for line in grplst:
    line = str(line)
    line = line.replace("Entry: ","")
    line = line.split(" ")
    line = line[0].split('/')
    grpline = line[0].replace('"','')
    alias = line[1]
    alias = alias.strip()

    #Get password for given alias
    # find any entry by its title
    val_entry = KeepassDB.find_entries(title=alias, first=True)
    val_entry 
    alias_id=alias_id.strip()
    alias_passwd=val_entry.password
    alias_passwd=alias_passwd.strip()
    alias_type=val_entry.notes
    alias_type=alias_type.strip()
#    print(alias_id)
#    print(alias_passwd)
#    print(alias_type)
    dic_alias.update({alias: (grpline,alias_id,alias_passwd,alias_type)})


cmd= 'echo "" > list.txt'
cmdtmp = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)

#create credentials keyring
for app_alias,val1 in dic_alias.items():
    cmd1= 'echo ' +app_alias+ ';' +dic_alias[app_alias][3]+ ' >> list.txt'
    cmd1tmp = subprocess.Popen(cmd1,shell=True, stdout=subprocess.PIPE)
    (cmd1output, cmd1outputerr) = cmd1tmp.communicate()



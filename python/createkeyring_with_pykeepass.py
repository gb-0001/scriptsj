#!/usr/bin/python3

import subprocess
import argparse
from pykeepass import PyKeePass

#pip3 install pykeepass
#./createkeyring_with_pykeepass.py -l keepassdb.kdbx -p 'PASSWORD' -g GRPKEEPASSFOLDER

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--list", required=True, type=str,
help="path list keepass user password keepassdb.kdbx")
ap.add_argument("-p", "--password", required=True, type=str,
help="define BDD keepass password")
ap.add_argument("-g", "--grpentry", required=True, type=str,
help="Define group example SQLLST")
ap.add_argument("-a", "--aliaspathlist", required=False, type=str,
help="define file path list.txt -a=/tmp  OPTION -a define create file list.txt with alias+type keepass and without -a create keyring ~/.local/share/python_keyring/keyring_pass.cfg")
args = vars(ap.parse_args())


KeepassDB= PyKeePass(args["list"], password=args["password"])


KeepassDBgroup = KeepassDB.find_groups(name=args["grpentry"], first=True)


grplst=KeepassDBgroup.entries

dic_alias={}
for line in grplst:
    line = str(line)
    line = line.replace("Entry: ","")
    line = line.split(" ")
    line = line[0].split('/')
    grpline = line[0].replace('"','')
    alias = line[1]
    alias = alias.strip()

    val_entry = KeepassDB.find_entries(title=alias, first=True)
    val_entry 
    alias_id=val_entry.username
    alias_id=alias_id.strip()
    alias_passwd=val_entry.password
    alias_passwd=alias_passwd.strip()
    alias_type=val_entry.notes
    alias_type=alias_type.strip()
#    print(alias_id)
#    print(alias_passwd)
#    print(alias_type)
    dic_alias.update({alias: (grpline,alias_id,alias_passwd,alias_type)})

if args["aliaspathlist"] is None:
    #create credentials keyring
    for app_alias,val1 in dic_alias.items():
        cmd1= '/usr/bin/python createcredentials.py -s=' +app_alias+ ' -u=' +dic_alias[app_alias][1]+ ' -p=' +dic_alias[app_alias][2]
        cmd1tmp = subprocess.Popen(cmd1,shell=True, stdout=subprocess.PIPE)
        (cmd1output, cmd1outputerr) = cmd1tmp.communicate()
else:
    pathfile= args["aliaspathlist"]+'/list.txt'
    file1 = open(pathfile, "w")
    file1 = open(pathfile, "a")
    #create credentials keyring
    for app_alias,val1 in dic_alias.items():
        txtreturn=""
        txtreturn=app_alias+';'+dic_alias[app_alias][3]
        file1.write(txtreturn+ "\n")
        
    file1.close()
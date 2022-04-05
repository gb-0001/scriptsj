#!/usr/bin/python

import argparse
from modules import md_auth_keyring

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--serviceid", required=True, type=str,
help="Define serviceid name define as app to find credentials")
args = vars(ap.parse_args())

login,password = md_auth_keyring.mdkeyring(args["serviceid"])

print("id: ", login)
print("pwd: ", password)

#./checkkeyring.py -s "appname" 

#!/usr/bin/python


# PREREQUIS:
# yum install python2-keyring ou yum install python3-keyring ou yum install python-pip puis pip install keyring
#
#EXAMPLE OF CALLING CREDENTIALS IN SCRIPTS
#import keyring
#try:
#    username = keyring.get_password('aliasapp', 'aliasapp_login')
#    password = keyring.get_password('aliasapp',username )
#except :
#    print("Credentials not found")
#print("username :", username)
#print("password :", password)
#
#Allows you to retrieve the list of credentials for the current session:
# python -c "import keyring.util.platform_; print(keyring.util.platform_.data_root())"


import argparse
import keyring
import getpass
import sys


class PasswordPromptAction(argparse.Action):
    def __init__(self,
             option_strings,
             dest=None,
             nargs=0,
             default=None,
             required=False,
             type=None,
             metavar=None,
             help=None):
        super(PasswordPromptAction, self).__init__(
             option_strings=option_strings,
             dest=dest,
             nargs=nargs,
             default=default,
             required=required,
             metavar=metavar,
             type=type,
             help=help)

    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)

#for automation pass -p with its password
#createcredentials.py -s SERVICE_ID -u mylogin -p mypwdscript
#Request the password in console
#createcredentials.py -s SERVICE_ID -u mylogin -i
# -d deletes the SERVICE_ID (credentialTag)
#createcredentials.py -s SERVICE_ID -u mylogin -d=deletetag


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--service_id", required=True, type=str,
help="Define the name of the credentials application to save credential Tag")
ap.add_argument("-u", "--login", required=True, type=str,
help="Define login")
#ap.add_argument("-p", "--passwordmode", required=True,
ap.add_argument("-p", "--passwordmodescript", required=False, type=str,
help="Define password as argument for scriptmode or directly in console inputmode")
ap.add_argument("-i", "--passwordmodeinput", action=PasswordPromptAction, type=str,
help="Set password directly in console inputmode")
ap.add_argument("-d", "--deletetag", required=False, type=str,
help="Define the credential TAG -s to delete it expected option -d=deletetag")
args = vars(ap.parse_args())


# Defines the name to retrieve credentials
service_id = args["service_id"]
# Defines the application login
username_app = args["login"]
# Allows not to display directly the login in clear text
username_app_key = service_id + '_login

password = ""
if args["deletetag"] == "deletetag" :
    keyring.delete_password(service_id,username_app)
    keyring.delete_password(service_id,username_app_key)
    print("credential tag is deleted")

other :
    if args["passwordmodeinput"] :
        password = args["passwordmodeinput"]
    if args["passwordmodescript"] :
        password = args["passwordmodescript"]
    if password == "" :
        print("Enter password")
        sys.exit()

    keyring.set_password(service_id, username, password)
    keyring.set_password(service_id, username_app_key, username_app)
    print( "The credential Tag to call is :", service_id , "The credential login to enter in the script is ", username_app_key )

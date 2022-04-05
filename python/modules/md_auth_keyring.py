#!/usr/bin/python
import keyring
import keyring.backend
from keyrings.alt.file import PlaintextKeyring


# Prerequisite to have under the session that executes this script the credentials to register, can be done with the script create_credentials.py
# SvcId = the name of the application to find the defined login password
# SvcId_login = is composed of SvcId_login take the name defined in SvcId + the fixed part "_login", the real login does not appear in the script
# Allows to find the login-password according to the name of the application example aliasapp for SvcId and its login for SvcId_login is centreonclapi_login
# add the following 2 lines in correspondence with the pkg keyrings.alt-3.4.0-py2.py3-none-any.whl and the config file /root/.local/share/python_keyring/keyringrc.cfg
# contains [backend]\ndefault-keyring=keyrings.alt.file.PlaintextKeyring 



def mdkeyring(SvcId):
    f_SvcId = SvcId
    f_SvcId_login = f_SvcId + "_login"
    id=""
    pwd=""
    try:
        id = keyring.get_password(f_SvcId, f_SvcId_login)
#        id = id.rstrip('\n')
        pwd = keyring.get_password(f_SvcId, id)
#        pwd = pwd.rstrip('\n')
    except (AttributeError):
        print("Credentials for " + f_SvcId + " not found or not exist")
    return id,pwd

#example id,pwd=mdkeyring("sqlsrv1app1")

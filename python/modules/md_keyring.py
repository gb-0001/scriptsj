#!/usr/bin/python
#GB-0001 github

import keyring
import keyring.backend
from keyrings.alt.file import PlaintextKeyring


#example login,passwd1=mdkeyring("keyringalias")
def mdkeyring(appId):
    md_appId = serviceid
    md_appId_login = md_appId + "_login"
    login1=""
    passwd1=""
    try:
        login1 = keyring.get_password(md_appId, md_appId_login)
#        login1 = login1.rstrip('\n')
        passwd1 = keyring.get_password(md_appId, login1)
#        passwd1 = passwd1.rstrip('\n')
    except (AttributeError):
        print("Credentials " + md_appId + " not found")
    return login1,passwd1

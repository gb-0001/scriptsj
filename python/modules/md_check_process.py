#!/usr/bin/python3
#GB-0001 github

import pidfile
import time

def mdcheckscriptalreadyrunning():
    print('Starting process')
    try:
        with pidfile.PIDFile():
            print('Process started')
            data="0"
            time.sleep(3)
            return data
    except pidfile.AlreadyRunningError:
        print('Already running.')
        data="1"
        return data
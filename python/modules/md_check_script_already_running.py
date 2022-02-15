#!/usr/bin/python3
#GB-0001 github

#check script already running

import socket
import sys
import time

def get_lock(process_name):
    # Without holding a reference to our socket somewhere it gets garbage
    # collected when the function exits
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        get_lock._lock_socket.bind('\0' + process_name)
        print('script socket lock start')
    except socket.error:
        print('script socket lock already exists')
        data="1"
        return data
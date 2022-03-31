#!/usr/bin/python
#GB-0001 github

import time

#Define in second the timestamp since epoch the date to check if it has exceeded the number of day with the current time
#Define in return 1 if the timestamp is superior to a number day
# returns 1 for the expiration of the date otherwise 0
def md_timestamp_date_expire(timestampSec,daynumber):
    epochrefnow = time.time()
    secdiff = int(epochrefnow) - int(timestampSec)
    secdaynumber = daynumber * 86400
    restetps = secdiff / 86400

    if secdiff > secdaynumber:
        dateexpire = 1
        #print ("number of day " , restetps)
    else:
        dateexpire  = 0
    return dateexpire


#result= md_timestamp_date_expire("1574066123",1)
#print (result)

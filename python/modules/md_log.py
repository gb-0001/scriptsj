#!/usr/bin/python
#GB-0001 github
import sys
import time
import logging
from logging.handlers import TimedRotatingFileHandler


######################init file
#
#init logfile path
def mdloginit(pathlogfile):
    logf=pathlogfile
    #Init and write file
    if not os.path.exists(logf):
        logs = open(logf, "w")
        logs.close()


############################# parameter Log Rotate

#number for the backupCount parameter 5 backup logs
#second (s)
#minute (m)
#hour (h)
#day (d)
#w0-w6 (weekday, 0=Monday)
#midnight
#timestamp using the strftime format %Y-%m-%d_%H-%M-%S

###########################################

###########################################
def mdcreate_timed_rotating_log(path,when1,interval1,backupCount1):
    """"""
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(path,
                                       when=when1,
                                       interval=interval1,
                                       backupCount=backupCount1)
                                    #    when="d",
                                    #    interval=30,
                                    #    backupCount=3)                                    
    logger.addHandler(handler)

#    for i in range(6):
#        logger.info("This is a test!")
#        time.sleep(75)
# mdcreate_timed_rotating_log(log_file_path)

#enable log rotate example:
#from modules import md_log 
#md_log.mdcreate_timed_rotating_log(pathlogfile,"d",30,3)

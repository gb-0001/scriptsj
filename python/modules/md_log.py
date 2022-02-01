#!/usr/bin/python
#GB-0001
import sys
import time
import logging
from logging.handlers import TimedRotatingFileHandler


######################Start init des fichiers
#
#initialise le chemin du fichier de log
def fxloginit(pathlogfile):
    logf=pathlogfile
    #Initialisation et ecrit le fichier
    if not os.path.exists(logf):
        logs = open(logf, "w")
        logs.close()


############################# Start Rotalion de la log
#
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
def fxcreate_timed_rotating_log(path,when1,interval1,backupCount1):
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
# fxcreate_timed_rotating_log(log_file_path)
############################# Fin  Rotalion de la log
#Active le fonctionnement de rotation de log en important le module md_log exemple from modules import md_log puis
#md_log.fxcreate_timed_rotating_log(pathlogfile,"d",30,3)
#
#############################Fin Rotalion de la log
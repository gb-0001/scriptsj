#!/usr/bin/python3
#GB-0001 github

import os
import sys
import mysql.connector

#BDD CNX
def md_mysqlreq(dbhostname,bddlogin,pwdbdd,dbname,dbport,sqlreq):
    try: 
        db_connection = mysql.connector.connect(
        host=dbhostname,
        user=bddlogin,
        password=pwdbdd,
        database=dbname,
        port=dbport
        )
    except: 
        print("Can't connect to database") 
        return 0
    print("BDD Connected:  OK") 
    # Making Cursor Object For Query Execution 
    cursor=db_connection.cursor() 
    # Executing Query 
    cursor.execute(sqlreq)
    lst=[]
    for x in cursor:
        lst.append(x)

    return lst

    # Closing Database Connection  
    db_connection.close() 
  
#### 
#req='SELECT s.cmd_line FROM services AS s INNER JOIN hosts AS h ON s.host_id = h.host_id WHERE s.desc = "CPU" AND h.name = "SPKZ0151";'
#return_req=mysqlreq("localhost",idbdd,pwdbdd,"BDNAME","3306",req)
#print(return_req)

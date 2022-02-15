#!/usr/bin/python3
#GB-0001 github

import os
import sys
import mysql.connector

#Bdd cnx

def mdmysqlrequest(dbhostname,idbdd,pwdbdd,dbname,dbport,sqlcmd):
    #Trying to connect  
    try: 
        db_connection = mysql.connector.connect(
        host=dbhostname,
        user=idbdd,
        password=pwdbdd,
        database=dbname,
        port=dbport
        )
    # If connection is not successful 
    except: 
        print("Can't connect to database") 
        return 0
    # If Connection Is Successful 
    print("Connected BDD OK") 
  
    # Making Cursor Object For Query Execution 
    cursor=db_connection.cursor() 
  
    # Executing Query 
    cursor.execute(sqlcmd)

    lst1=[]
    for x in cursor:
        lst1.append(x)

    return lst1

    # Closing Database Connection  
    db_connection.close() 
  
####EXAMPLE Function Call For Connecting To Our Database 
#req='SELECT s.command_line FROM services AS s INNER JOIN hosts AS h ON s.host_id = h.host_id WHERE s.description = "CpuL" AND h.name = "srv1";'
#req=mdmysqlrequest("localhost",idbdd,pwdbdd,"DBNAME","3306",req)
#print(req)

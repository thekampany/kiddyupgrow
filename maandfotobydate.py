#!/usr/bin/env python

#for every yyyymm from birthdate of oldest person until today
#get files from subfolders
#and populate table with imagefilenames that match the yyyymm

import glob
import os.path
import sqlite3
import time

curyear = int(time.strftime("%Y"))
curmonth = int(time.strftime("%m"))

path1 = '/home/pi/maandfotos/naam1/*.*'
path2 = '/home/pi/maandfotos/naam2/*.*'
path3 = '/home/pi/maandfotos/naam3/*.*'
folder1 = 'naam1'
folder2 = 'naam2'
folder3 = 'naam3'
file1 = ''
file2 = ''
file3 = ''
blank = 'blank.jpg'

conn = sqlite3.connect('maandfotos.db')

conn.executescript('drop table if exists SORTEDBYDATE;')

conn.execute('''CREATE TABLE SORTEDBYDATE
        (YM TEXT PRIMARY KEY     NOT NULL,
        FOLDER1        CHAR(255),
        FILE1          CHAR(50),
        FOLDER2        CHAR(250),
        FILE2          CHAR(50),
        FOLDER3        CHAR(250),
        FILE3          CHAR(50));''')
#print "Table created successfully"

 
def month_year_iter( start_month, start_year, end_month, end_year ):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end ):
        y, m = divmod( ym, 12 )
        yield str(y)+str(m+1).zfill(2)

for ym in month_year_iter(01,2002, curmonth, curyear):
    print ym
    conn.execute("INSERT INTO SORTEDBYDATE (YM) VALUES (?)",[ym])
    conn.commit
    conn.execute("UPDATE SORTEDBYDATE SET FOLDER1 = ?, FILE1 = ? WHERE YM=?",(folder1, blank, ym))
    conn.commit()
    files=glob.glob(path1)  
    for file in files:    
        file1 = blank
        if os.path.basename(file)[0:6] == ym: 
          file1 = os.path.basename(file)
          print file1
          conn.execute("UPDATE SORTEDBYDATE SET FOLDER1 = ?, FILE1 = ? WHERE YM=?",(folder1, file1, ym))
          conn.commit()

for ym in month_year_iter(01,2002, curmonth,curyear):
    conn.execute("UPDATE SORTEDBYDATE SET FOLDER2 = ?, FILE2 = ? WHERE YM=?",(folder2, blank, ym))
    conn.commit()
    files2=glob.glob(path2)
    for file in files2:
        if os.path.basename(file)[0:6] == ym:
          file2 = os.path.basename(file)
          print file2
          conn.execute("UPDATE SORTEDBYDATE SET FOLDER2 = ?, FILE2 = ? WHERE YM=?",(folder2, file2, ym))
          conn.commit()

for ym in month_year_iter(01,2002, curmonth,curyear):
    conn.execute("UPDATE SORTEDBYDATE SET FOLDER3 = ?, FILE3 = ? WHERE YM=?",(folder3, blank, ym))
    conn.commit()
    files3=glob.glob(path3)
    for file in files3:
        if os.path.basename(file)[0:6] == ym:
          file3 = os.path.basename(file)
          print file3
          conn.execute("UPDATE SORTEDBYDATE SET FOLDER3 = ?, FILE3 = ? WHERE YM=?",(folder3, file3, ym))
          conn.commit()

conn.close()


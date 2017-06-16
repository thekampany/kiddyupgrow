#!/usr/bin/env python

#for inputfolders 
#that have images with filename yyyymmxxxx.jpg
#determine age in months of person on image
#put age and filename and path in table 
#for retrieval by webpage
#todo: number of persons 2 or 3 or 4...?

import glob
import os.path
import sqlite3

path1 = '/home/pi/maandfotos/naam1/*.*'
path2 = '/home/pi/maandfotos/naam2/*.*'
path3 = '/home/pi/maandfotos/naam3/*.*'
folder1 = 'naam1'
folder2 = 'naam2'
folder3 = 'naam3'
file1 = ''
file2 = ''
file3 = ''
bdate1 = '2002-01-01'
bdate2 = '2005-02-01'
bdate3 = '2009-09-01'
blankfile = 'blank.jpg'

conn = sqlite3.connect('maandfotos.db')

conn.executescript('drop table if exists SORTEDBYAGE;')
conn.execute('''CREATE TABLE SORTEDBYAGE
        (AGE INT PRIMARY KEY     NOT NULL,
        FOLDER1        CHAR(255),
        FILE1          CHAR(50),
        FOLDER2        CHAR(250),
        FILE2          CHAR(50),
        FOLDER3        CHAR(250),
        FILE3          CHAR(50));''')

from datetime import datetime
from dateutil import relativedelta
import time

#populate table with age in month rows up until age-in-months for oldest
curyear = time.strftime("%Y")
curmonth = time.strftime("%m")
date1 = datetime.strptime(str(curyear+'-'+curmonth+'-01'), '%Y-%m-%d')
date2 = datetime.strptime(str(bdate1), '%Y-%m-%d')
r = relativedelta.relativedelta(date1, date2)
age = (r.years * 12) + r.months
i = 0
while (i < age):
    conn.execute("INSERT INTO SORTEDBYAGE (AGE) VALUES (?)",[i])
    conn.commit()
    i = i + 1
i = 0
while (i < age):
    conn.execute("UPDATE SORTEDBYAGE SET FOLDER1 = ?, FILE1 = ?, FOLDER2 = ?, FILE2 = ?, FOLDER3 =?, FILE3 =? WHERE AGE=?", (folder1, blankfile, folder2, blankfile, folder3, blankfile, i))
    conn.commit()
    i = i + 1


#loop through files per person to determine age and populate the table
files=glob.glob(path1)  
for file in files:    
    print file
    first6 = unicode(os.path.basename(file)[0:6],'utf-8')
    if first6.isnumeric():
       date1 = datetime.strptime(str(os.path.basename(file)[0:6]+"01"), '%Y%m%d')
       date2 = datetime.strptime(str(bdate1), '%Y-%m-%d')
       r = relativedelta.relativedelta(date1, date2)
       age = (r.years * 12) + r.months
       print age
       file1 = os.path.basename(file)
       conn.execute("UPDATE SORTEDBYAGE SET FOLDER1 = ?, FILE1 = ? WHERE AGE=?",(folder1, file1, age))
       conn.commit()


files=glob.glob(path2)
for file in files:
    print file
    first6 = unicode(os.path.basename(file)[0:6],'utf-8')
    if first6.isnumeric():
       date1 = datetime.strptime(str(os.path.basename(file)[0:6]+"01"), '%Y%m%d')
       date2 = datetime.strptime(str(bdate2), '%Y-%m-%d')
       r = relativedelta.relativedelta(date1, date2)
       age = (r.years * 12) + r.months
       print age
       file2 = os.path.basename(file)
       conn.execute("UPDATE SORTEDBYAGE SET FOLDER2 = ?, FILE2 = ? WHERE AGE=?",(folder2, file2, age))
       conn.commit()


files=glob.glob(path3)
for file in files:
    print file
    first6 = unicode(os.path.basename(file)[0:6],'utf-8')
    if first6.isnumeric():
       date1 = datetime.strptime(str(os.path.basename(file)[0:6]+"01"), '%Y%m%d')
       date2 = datetime.strptime(str(bdate3), '%Y-%m-%d')
       r = relativedelta.relativedelta(date1, date2)
       age = (r.years * 12) + r.months
       print age
       file3 = os.path.basename(file)
       conn.execute("UPDATE SORTEDBYAGE SET FOLDER3 = ?, FILE3 = ? WHERE AGE=?",(folder3, file3, age))
       conn.commit()


conn.close()


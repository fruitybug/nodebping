import sqlite3
from datetime import datetime
import os.path
from subprocess import PIPE, run

#create DB if not exist:
def createDB ():
    conn = sqlite3.connect('PingDB.db')
    conn.execute('''CREATE TABLE NODEB ([Date] date, [Time] time, [Host] text, [min] float, [avg] float, [max] float, [mdev] float, [Packet size] decimal)''')
    conn.commit()
    conn.close()

if os.path.exists('PingDB.db'):
    print("DB exits")
else:
    createDB()

#host IP to array:
hosts = []

with open('nodeb.txt', 'r') as file_nodeb:
    hosts = file_nodeb.read().splitlines()

def ping(ip):
    command = ['ping', "-c3", str(ip)]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    try:
        result = result.stdout.split("\n")[7].split(" ")[3].split("/")
        print("Host: "+ip, " min: " +result[0], " avg: "+result[1], " min: "+result[2], " mdev: "+result[3])

        date = datetime.now().strftime('%d.%m.%Y')
        time = datetime.now().strftime('%H:%M:%S')

        conn = sqlite3.connect('PingDB.db')
        sql = ("""INSERT INTO 'NODEB' ('Date', 'Time', 'Host', 'min', 'avg', 'max', 'mdev') VALUES (?,?,?,?,?,?,?);""")
        sqldata = (date, time, ip, result[0], result[1], result[2], result[3])
        conn.execute(sql, sqldata)
        conn.commit()
        conn.close()           
    except IndexError:
        print("fail ping host:"+ip)

for ip in hosts:
    ping(ip)   
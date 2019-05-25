import sqlite3
import sys

dbname = './database/sensorData.db'


def insertData(temp, hum):
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("INSERT INTO DHT_data(temp, hum) values((?), (?))", (temp, hum))
    conn.commit()
    conn.close()


def selectLast24HData():
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("SELECT * "
                 "FROM DHT_data "
                 "where timestamp > datetime('now', 'localtime', '-24 hours') "
                 "ORDER BY timestamp DESC")
    data = curs.fetchall()
    conn.close()
    times = []
    temps = []
    hums = []
    for row in reversed(data):
        times.append(row[0])
        temps.append(row[1])
        hums.append(row[2])
    return times, temps, hums

#!/bin/sh
DBNAME="../sensorData.db"
sqlite3 $DBNAME "SELECT *
                FROM DHT_data
                where timestamp > datetime('now', 'localtime', '-1 minutes')
                ORDER BY timestamp DESC;"

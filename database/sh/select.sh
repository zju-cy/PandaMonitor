#!/bin/sh
DBNAME="../sensorData.db"
sqlite3 $DBNAME "SELECT * FROM DHT_data;"
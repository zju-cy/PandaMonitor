#!/bin/sh
rm -f ../sensorData.db
echo "Begin creat table..."
sqlite3 ../sensorData.db < ../sql/create.sql
echo "Creat table finish"
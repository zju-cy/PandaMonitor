#!/bin/sh
echo "Begin insert data..."
sqlite3 ../sensorData.db < ../sql/insert.sql
echo "Finish insert data"
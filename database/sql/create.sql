CREATE TABLE DHT_data
(
    timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
    temp NUMERIC,
    hum NUMERIC
);
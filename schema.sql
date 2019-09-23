CREATE TABLE users (
id TEXT PRIMARY KEY,
name TEXT NOT NULL,
email TEXT UNIQUE NOT NULL,
profile_pic TEXT NOT NULL
);

CREATE TABLE sensors (
sensor_id TEXT PRIMARY KEY,
user_id TEXT NOT NULL,
sensor_name TEXT NOT NULL,
sensor_type TEXT NOT NULL
);
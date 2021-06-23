-- Copyright (c) 2021 Veera Lupunen

BEGIN;

CREATE TABLE IF NOT EXISTS worker (
	id SERIAL PRIMARY KEY, 
	username VARCHAR(255) UNIQUE NOT NULL, 
	password TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS entry (
	id SERIAL PRIMARY KEY, 
	time_beg TIMESTAMP NOT NULL, 
	time_end TIMESTAMP, 
	pause INTEGER, 
	notes TEXT);

CREATE TABLE IF NOT EXISTS task (
	id SERIAL PRIMARY KEY, 
	content TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS worker_entry (
	u_id INTEGER REFERENCES worker(id) ON UPDATE CASCADE ON DELETE CASCADE, 
	e_id INTEGER REFERENCES entry(id) ON UPDATE CASCADE ON DELETE CASCADE);
	
CREATE TABLE IF NOT EXISTS task_entry (
	t_id INTEGER REFERENCES task(id) ON UPDATE CASCADE ON DELETE CASCADE, 
	e_id INTEGER REFERENCES entry(id) ON UPDATE CASCADE ON DELETE CASCADE);	
	
COMMIT;

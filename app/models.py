import os

import psycopg2

dbasename = os.environ.get('DBASE_NAME')
dbaseuser = os.environ.get('DBASE_USER')
dbasepass = os.environ.get('DBASE_PASS')
dbasehost = os.environ.get('DBASE_HOST')

conn = psycopg2.connect("dbname={} user={} password={} host={} port={}".format(dbasename, dbaseuser, dbasepass, dbasehost, ))  # Connecting to the database
cur = conn.cursor()  # Activate connection using the cursor


cur.execute('''CREATE TABLE IF NOT EXISTS questions(
    id serial PRIMARY KEY,
    title varchar (50) NOT NULL,
    description varchar (100) NOT NULL,
    timestamp timestamp default current_timestamp
    ) ''')

cur.execute('''CREATE TABLE IF NOT EXISTS users(
    id serial PRIMARY KEY,
    username varchar (50) NOT NULL,
    email varchar (100) NOT NULL,
    password varchar (100) NOT NULL,
    password_confirmation varchar (100) NOT NULL,
    timestamp timestamp default current_timestamp
    ) ''')

cur.execute('''CREATE TABLE answers(
    id serial PRIMARY KEY,
    description text NOT NULL,
    timestamp timestamp default current_timestamp
    ) ''')

cur.execute('''CREATE TABLE questions(
    id serial PRIMARY KEY,
    title text NOT NULL,
    description text NOT NULL,
    timestamp timestamp default current_timestamp
    ) ''')


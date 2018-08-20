import psycopg2

conn = psycopg2.connect("dbname=stackoverflowlite user=postgres password=adminray host=localhost")  # Connecting to the database
cur = conn.cursor()  # Activate connection using the cursor

cur.execute('''CREATE TABLE IF NOT EXISTS questions(
    id serial PRIMARY KEY,
    title varchar (50) NOT NULL,
    description varchar (100) NOT NULL,
    timestamp timestamp default current_timestamp
    ) ''')

cur.execute('''CREATE TABLE IF NOT EXISTS answers(
    id serial PRIMARY KEY,
    description varchar (200) NOT NULL,
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

conn.commit()

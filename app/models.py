import psycopg2

conn = psycopg2.connect("dbname=d35r4tfslcr7uf user=hantjxrfgrzzrr password=d6a32d0baa1e998ef650ff3ecc05a427eca2595631125cc23d19526779398203 host=ec2-54-221-237-246.compute-1.amazonaws.com port=5432")  # Connecting to the database
cur = conn.cursor()  # Activate connection using the cursor


cur.execute('''CREATE TABLE IF NOT EXISTS users(
    id serial PRIMARY KEY,
    username varchar (50) NOT NULL,
    email varchar (100) NOT NULL,
    password varchar (100) NOT NULL,
    password_confirmation varchar (100) NOT NULL,
    timestamp timestamp default current_timestamp
    ) ''')

cur.execute('''CREATE TABLE IF NOT EXISTS answers(
    id serial PRIMARY KEY,
    description text (200) NOT NULL,
    timestamp timestamp default current_timestamp
    ) ''')

cur.execute('''CREATE TABLE IF NOT EXISTS questions(
    id serial PRIMARY KEY,
    title varchar (100) NOT NULL,
    description text (1100) NOT NULL,
    timestamp timestamp default current_timestamp
    ) ''')


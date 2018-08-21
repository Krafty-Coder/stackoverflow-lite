import psycopg2

conn = psycopg2.connect("dbname=stackoverflowlite user=postgres password=adminray host=localhost")  # Connecting to the database
cur = conn.cursor()  # Activate connection using the cursor

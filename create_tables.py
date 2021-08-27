import os

import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
sslmode = 'require' if 'HEROKU' in os.environ else 'disable'
conn = psycopg2.connect(DATABASE_URL, sslmode=sslmode)

cur = conn.cursor()
cur.execute(open('database.sql', 'r').read())
conn.commit()

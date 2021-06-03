import psycopg2
conn = psycopg2.connect("host=172.17.0.1 port=5432 dbname=meteo user=danirr password=52590")
cur = conn.cursor()
with open('tmeteo2020_09_02.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f, 'meteoprueba', sep=';')

conn.commit()
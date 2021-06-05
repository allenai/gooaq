import psycopg2
import os

def connect_to_gcp():
    host = 'aa.bb.cc.dd' # IP to your database
    conn = psycopg2.connect(
        host=host,
        port=1234, # port to your DB
        dbname='dbname', # DB name
        user='dbuser', # username for your database
        password=os.getenv('DO_DB_PASSWORD')) # password to your database
    cur = conn.cursor()

    return conn, cur

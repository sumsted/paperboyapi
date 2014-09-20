__author__ = 'scottumsted'
"""
copied from antipool example on ibm site and replaced with psycopg pooling
added logging and max tries
USAGE:
from webapp_pool import get_connection
conn, cur = get_connection()   # Might hang, but never raises
cur.execute(SQL)
conn.commit()
conn.release()    # 'conn.release()' not 'conn.close()'
"""
import yaml, os
from time import sleep
import psycopg2
from psycopg2 import extras
from psycopg2 import pool
import logging

yaml_file = open(os.getenv('PAPERBOY_YAML',''))
settings = yaml.load(yaml_file)
yaml_file.close()

host = settings['PAPERBOY_DB_HOST']
database = settings['PAPERBOY_DB']
maxConnections = settings['PAPERBOY_DB_MAX_CONNECTIONS']
user = settings['PAPERBOY_DB_USER']
password = settings['PAPERBOY_DB_PASSWORD']
maxTries = settings['PAPERBOY_DB_MAX_TRIES']

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
conn_pool = pool.ThreadedConnectionPool(minconn=1, maxconn=maxConnections, host=host, database=database, user=user, password=password)

def put_connection(conn):
    conn_pool.putconn(conn=conn)

def get_connection():
    got_connection = False
    conn = None
    cur = None
    t = 1
    while not got_connection:
        try:
            conn = conn_pool.getconn()
            cur = conn.cursor(cursor_factory = extras.RealDictCursor)
            got_connection = True
        except psycopg2.OperationalError, mess:
            # Might log exception here
            logging.warning('%s - try %d'%(mess,t))
            t += 1
            if t>maxTries :
                logging.error('too many tries')
                exit()
            sleep(1)
        except AttributeError, mess:
            logging.warning('%s - try %d'%(mess,t))
            t += 1
            if t>maxTries :
                logging.error('too many tries')
                exit()
            sleep(1)
    return conn, cur


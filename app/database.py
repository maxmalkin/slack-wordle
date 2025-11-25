import psycopg2
import os
from typing import Optional

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

def close_db_connection(conn):
    if conn:
        conn.close()

def execute_query(query: str, params: Optional[tuple] = None, fetch: bool = False):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)

        if fetch:
            result = cur.fetchall()
            cur.close()
            return result
        else:
            conn.commit()
            cur.close()
    finally:
        close_db_connection(conn)

def execute_query_one(query: str, params: Optional[tuple] = None):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchone()
        cur.close()
        return result
    finally:
        close_db_connection(conn)

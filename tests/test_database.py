import pytest
from app.database import get_db_connection, close_db_connection

def test_get_db_connection():
    conn = get_db_connection()
    assert conn is not None
    assert not conn.closed
    close_db_connection(conn)
    assert conn.closed

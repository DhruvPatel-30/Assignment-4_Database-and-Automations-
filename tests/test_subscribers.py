import os
import time
import pymysql
import pytest
from uuid import uuid4

# Use environment variables if provided by CI, otherwise defaults
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3307))
DB_NAME = os.getenv("DB_NAME", "subscriptions_dhruv")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "DhruvPass!9062297")

def get_conn(retries=10, delay=1):
    for _ in range(retries):
        try:
            return pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER,
                                   password=DB_PASSWORD, database=DB_NAME,
                                   cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        except Exception:
            time.sleep(delay)
    raise RuntimeError("Could not connect to DB")

def test_crud_subscriber():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # CREATE
            unique = str(uuid4())[:8]
            name = f"Dhruv-{unique}"
            email = f"dhruv9062297+{unique}@test.com"
            phone = "111-222-3333"
            cur.execute("INSERT INTO subscribers (name, email, phone) VALUES (%s, %s, %s)",
                        (name, email, phone))
            inserted_id = cur.lastrowid
            assert inserted_id is not None

            # READ
            cur.execute("SELECT * FROM subscribers WHERE id=%s", (inserted_id,))
            row = cur.fetchone()
            assert row["email"] == email
            assert row["name"] == name

            # UPDATE
            new_name = name + "-updated"
            cur.execute("UPDATE subscribers SET name=%s WHERE id=%s", (new_name, inserted_id))
            cur.execute("SELECT name FROM subscribers WHERE id=%s", (inserted_id,))
            row = cur.fetchone()
            assert row["name"] == new_name

            # DELETE
            cur.execute("DELETE FROM subscribers WHERE id=%s", (inserted_id,))
            cur.execute("SELECT * FROM subscribers WHERE id=%s", (inserted_id,))
            row = cur.fetchone()
            assert row is None
    finally:
        conn.close()

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://api_user:api_pass@postgres:5432/api_lab')


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return g.db


def close_db(error):
    db = g.pop('db', None)
    if db:
        db.close()


def query_db(query, args=None):
    if args is None:
        args = ()
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(query, args)
        rv = cur.fetchall()
    except Exception as e:
        rv = []
    cur.close()
    return rv


def execute_db(query, args=None):
    if args is None:
        args = ()
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(query, args)
        db.commit()
    except Exception:
        db.rollback()
    cur.close()


def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
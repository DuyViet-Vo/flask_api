import sqlite3

conn = sqlite3.connect("books.db")

cursor = conn.cursor()
sql_query = """ Create table book (
    id INTEGER PRIMARY KEY,
    author text NOT NULL,
    title text NOT NULL
)"""
cursor.execute(sql_query)
import sqlite3
from datetime import datetime, timedelta


def init_db(db_file):
    con = sqlite3.connect("/db/templatedb.db")
    print("Database opened successfully")

    con.execute("""
                DROP TABLE IF EXISTS users
            """)

    con.execute("""
                DROP TABLE IF EXISTS blog
            """)

    con.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    urole TEXT NOT NULL
                )
            """)

    con.execute("""
                CREATE TABLE blog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            """)

    '''
    con.execute("""
                CREATE TABLE admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    bio TEXT NOT NULL
                )
            """)
    '''
    populatedb(con)

    print("successfully create table")
    con.close()

def populatedb(con):
    print("Populating database...\n")
    con.execute("""
        INSERT INTO users (username, email, password, urole)
        VALUES("admin", "admin@localhost.com", "This-Is-The-Admin-Password-XD!", "admin")
        """)

    con.execute("""
        INSERT INTO blog (author, title, content)
        VALUES("admin", "FUCKKKKK", "okay")
        """)

    con.commit()
    return

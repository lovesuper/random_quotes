import sqlite3

database = "quotes.sqlite.db"


if __name__ == "__main__":
    with sqlite3.connect(database) as c:
        cur = c.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY, 
            text TEXT NOT NULL,
            parsed_id VARCHAR NOT NULL
        );
        """)

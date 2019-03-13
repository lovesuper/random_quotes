import sqlite3
from json import dumps

from bottle import run, response, Bottle

from db import database

app = Bottle()


def dict_factory(cursor, row):
    dictionary = {}
    for idx, column in enumerate(cursor.description):
        dictionary[column[0]] = row[idx]

    return dictionary


@app.route("/quotes")
def get_quotes():
    response.content_type = "application/json"
    with sqlite3.connect(database) as c:
        c.row_factory = dict_factory
        cur = c.cursor()
        cur.execute("SELECT text, parsed_id FROM quotes WHERE id IN "
                    "(SELECT id FROM quotes ORDER BY RANDOM() LIMIT 100);")
        quotes = cur.fetchall()

        return dumps(quotes)


run(app, host="127.0.0.1", port=8181)

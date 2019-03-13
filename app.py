from json import dumps

from bottle import run, response, Bottle
from sqlalchemy import func

from db import DBSession, Quote

app = Bottle()


@app.route("/quotes")
def get_quotes():
    response.content_type = "application/json"
    session = DBSession()
    quotes = session.query(Quote).order_by(func.random()).all()

    return dumps(list(map(lambda x: x.jsonify(), quotes)))


run(app, host="127.0.0.1", port=8181)

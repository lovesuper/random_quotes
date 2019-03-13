import os
from json import dumps

from bottle import run, response, Bottle
from sqlalchemy import func

from db import DBSession, Quote

app = application = Bottle()


@app.route("/")
def root():
    return "Welcome!"


@app.route("/quotes")
def get_quotes():
    response.content_type = "application/json"
    session = DBSession()
    quotes = session.query(Quote).order_by(func.random()).all()

    return dumps(list(map(lambda x: x.jsonify(), quotes)))


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)

from json import dumps

from bottle import run, response, Bottle, request
from sqlalchemy import func

from db import DBSession, Quote

app = Bottle()


@app.route("/")
def root():
    return ("Use `/quotes` endpoint with optional `limit` and `offset` query parameters "
            "to get some random quotes from `bash.im`, `zadolba.li` or `ithappens.me`.")


@app.route("/quotes")
def get_quotes():
    response.content_type = "application/json"
    limit = request.query.limit or 100
    offset = request.query.offset or 0

    try:
        limit = int(limit)
        offset = int(offset)
        assert 0 <= int(limit) <= 1000 or 0 < int(offset)
    except Exception:
        return dumps({"Error": "Too much you wish."})

    session = DBSession()
    quotes = session.query(Quote).order_by(func.random()).limit(limit).offset(offset).all()

    return dumps(list(map(lambda x: x.jsonify(), quotes)))


if __name__ == '__main__':
    run(app, host="127.0.0.1", port=8181)

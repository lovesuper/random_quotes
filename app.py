import re
from json import dumps

from bottle import run, response, Bottle
from bs4 import BeautifulSoup
from requests import get


def remove_tags(text):
    return re.compile(r"<[^>]+>").sub("", text)


app = Bottle()

ITHAPPENS = "https://ithappens.me/random"
BASHIM = "https://bash.im/random"
ZADOLBALI = "https://zadolba.li/"


@app.route("/ithappens")
def ithappens():
    response.content_type = "application/json"
    r = get(ITHAPPENS)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("div", attrs={"class": "story"})
    result = []
    for article in articles:
        quote_body = article.find("div", attrs={"class": "text"}).text
        quote_body = remove_tags(quote_body).replace("&quot;", "\"").replace("  ", "").strip()
        id_ = article.find("div", attrs={"class": "id"}).text.strip()
        result.append({"id": id_, "text": quote_body})

    return dumps(result)


@app.route("/bashim")
def bashim():
    response.content_type = "application/json"
    r = get(BASHIM)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("div", attrs={"class": "quote__frame"})
    result = []
    for article in articles:
        quote_body = article.find("div", attrs={"class": "quote__body"}).text
        quote_body = remove_tags(quote_body).replace("&quot;", "\"").replace("  ", "").strip()
        *_, id_ = article.find("a", attrs={"class": "quote__header_permalink"}).text,
        result.append({"id": id_, "text": quote_body})

    return dumps(result)


@app.route("/zadolbali")
def zadolbali():
    response.content_type = "application/json"
    r = get(ZADOLBALI)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("div", attrs={"class": "story"})
    result = []
    for article in articles:
        quote_body = article.find("div", attrs={"class": "text"}).text
        quote_body = (
            remove_tags(quote_body).
            replace("&quot;", "\"").
            replace("  ", "").
            replace(" ", "").strip()
        )
        *_, id_ = article.find("h2"). find("a"). get("href"). split("/")
        result.append({"id": id_, "text": quote_body})

    return dumps(result)


run(app, host="127.0.0.1", port=8181)

import re
import sqlite3
from time import sleep

from bs4 import BeautifulSoup
from requests import get

from db import database

ITHAPPENS = "https://ithappens.me/random"
BASHIM = "https://bash.im/random"
ZADOLBALI = "https://zadolba.li/"


def remove_tags(text):
    return re.compile(r"<[^>]+>").sub("", text)


def parse_ithappens():
    response = get(ITHAPPENS)
    soup = BeautifulSoup(response.content, "html.parser")
    quotes = []
    articles = soup.find_all("div", attrs={"class": "story"})
    for article in articles:
        quote_body = article.find("div", attrs={"class": "text"}).text
        quote_body = remove_tags(quote_body).replace("&quot;", "\"").replace("  ", "").strip()
        id_ = article.find("div", attrs={"class": "id"}).text.strip()
        quotes.append({"id": id_, "text": quote_body})

    return quotes


def parse_bashim():
    r = get(BASHIM)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("div", attrs={"class": "quote__frame"})
    quotes = []
    for article in articles:
        quote_body = article.find("div", attrs={"class": "quote__body"}).text
        quote_body = remove_tags(quote_body).replace("&quot;", "\"").replace("  ", "").strip()
        *_, id_ = article.find("a", attrs={"class": "quote__header_permalink"}).text,
        quotes.append({"id": id_, "text": quote_body})

    return quotes


def parse_zadolbali():
    r = get(ZADOLBALI)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("div", attrs={"class": "story"})
    quotes = []
    for article in articles:
        quote_body = article.find("div", attrs={"class": "text"}).text
        quote_body = (
            remove_tags(quote_body).
            replace("&quot;", "\"").
            replace("  ", "").
            replace(" ", "").strip()
        )
        *_, id_ = article.find("h2"). find("a"). get("href"). split("/")
        quotes.append({"id": id_, "text": quote_body})

    return quotes


def parse_quotes(times, delay):
    quotes = []
    for _ in range(times):
        quotes.extend(parse_bashim())
        quotes.extend(parse_ithappens())
        quotes.extend(parse_zadolbali())
        sleep(delay)

    with sqlite3.connect(database) as c:
        cur = c.cursor()
        cur.executemany("INSERT INTO quotes(text, parsed_id) VALUES (?, ?);",
                        map(lambda x: (x['text'], x['id']), quotes))


if __name__ == "__main__":
    parse_quotes(times=5, delay=1)

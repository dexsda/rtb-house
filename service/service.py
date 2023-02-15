# coding: utf-8
import requests
from flask import Flask
from flask_caching import Cache
from bs4 import BeautifulSoup

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
cache.set('lastBuildDate', None)

JOKE_AMOUNT = 100


def get_latest_date():
    req = requests.get("http://bash.org.pl/rss")
    soup = BeautifulSoup(req.content, 'html.parser')
    print(soup.prettify())
    return str(soup.find("lastbuilddate").contents)


def page_updated():
    latest_date = get_latest_date()
    if latest_date != cache.get('lastBuildDate'):
        cache.set('lastBuildDate', latest_date)
        return True
    return False


def parse_page(page):
    jokes = list()
    req = requests.get(f"http://bash.org.pl/latest/?page={page}")
    soup = BeautifulSoup(req.content, 'html.parser')
    for quote in soup.find_all("div", class_="q post"):
        jokes.append({
            'id': '2',
            'msg': str(quote.find(
                "div",
                class_="quote post-content post-body"
            ).encode_contents())
        })

    return jokes


def get_latest_jokes(joke_amount=JOKE_AMOUNT):
    page = 1
    jokes = []
    while len(jokes) < joke_amount:
        jokes.extend(parse_page(page))
        page += 1
    return jokes


def joke_list():
    if page_updated():
        cache.set('jokes', get_latest_jokes())
    return cache.get('jokes')


@app.route("/jokes/", methods=["GET"])
def full_list():
    return joke_list()


@app.route("/jokes/<num>", methods=["GET"])
def single_item(num):
    try:
        return joke_list()[int(num)]
    except IndexError:
        return {"error": "there aren't that many jokes"}
    except ValueError:
        return {"error": "index must be an integer"}


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")

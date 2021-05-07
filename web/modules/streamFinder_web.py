#!/usr/bin/python3.7
import sys
from flask import Flask, render_template, request
sys.path.insert(1, "/var/www/html/streamFinder/sources")
from main import search_movie
sys.path.insert(1, "/var/www/html/streamFinder/web/modules/")
app = Flask(__name__)


@app.route("/", methods = ['GET'])
def home():
    return render_template("home.html")

@app.route("/", methods = ['POST'])
def resultat():
    result = request.form
    title = result['name']

    sources = "DE"

    lang = "fr"

    links_garb, links_ext = search_movie(title, sources=sources, lang=lang, nbRes=30 )

    links = links_garb | links_ext
    return render_template("resultat.html", resultat=links, name=title)


if __name__ == "__main__":
    app.run()

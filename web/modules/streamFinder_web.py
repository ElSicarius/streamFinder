#!/usr/bin/python3.7
import sys
from flask import Flask, render_template, request, Response
from functools import wraps
import json
sys.path.insert(1, "/var/www/html/streamFinder/")
from sources.main import search_movie
sys.path.insert(1, "/var/www/html/streamFinder/web/modules/")
app = Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/", methods = ['GET'])
@requires_auth
def home():
    return render_template("home.html")

@app.route("/", methods = ['POST'])
@requires_auth
def resultat():
    result = request.form.to_dict()
    title = result['name']
    sources = str()
    result.setdefault("google",str())
    result.setdefault("duckduckgo",str())
    result.setdefault("external",str())
    sources += result["google"]
    sources += result["duckduckgo"]
    sources += result["external"]
    lang = result['lang']

    links_garb, links_ext, raw_websites = search_movie(title, sources=sources, lang=lang, nbRes=30 )

    print("Search for", title, links_garb, links_ext, raw_websites)
    links_ext = [(erf,erf.split(";")[1]) for erf in links_ext]
    return render_template("resultat.html",
                            resultat_garb=links_garb,
                            resultat_ext=links_ext,
                            resultats_raw=raw_websites,
                            name=title)


if __name__ == "__main__":
    app.run()

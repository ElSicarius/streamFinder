#!/usr/bin/python3.7
import sys
from flask import Flask, render_template, request, Response, url_for, redirect
from functools import wraps
import json
import uuid
import re
import pathlib

path = str(pathlib.Path(__file__).parent.absolute()).split("streamFinder")[0]
sys.path.insert(1, path+"streamFinder/")
from sources.main import search_movie
sys.path.insert(1, path+"streamFinder/web/modules/")

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

    #print("Search for", title, links_garb, links_ext, raw_websites)
    links_ext = [(erf,erf.split(";")[1]) for erf in links_ext]
    # uniq id
    id_ = str(uuid.uuid4().hex)

    print(f"writting /tmp/streamFinder_{id_}.log")
    results = {"title": title,
            "garb": list(links_garb),
            "ext": list(links_ext),
            "raw": list(raw_websites),
            "id": id_}
    with open(f"/tmp/streamFinder_{id_}.log", "w") as f:
        print(results)
        f.write(json.dumps(results))
    return redirect(url_for('.get_results', id=id_))

@app.route("/results", methods = ['GET'])
@requires_auth
def get_results():
    id_ = str(request.args.get("id"))
    id_ = re.findall("[A-Za-z\d]+", id_)
    if not id_:
        return render_template("home.html")
    id_ = id_[0]
    table = {"garb": [],
            "ext": [],
            "raw": []}
    try:
        with open(f"/tmp/streamFinder_{id_}.log", "r") as f:
            try:
                table.update(json.loads(f.read()))
                title = table["title"]
            except Exception as e :
                print(f"Error in retrieving data -> {e}")
                links = []
                title = "Couldn't find your results with this id"
    except FileNotFoundError :
        print(f"Tried to find file with id {id_} but failed")
        title = "Couldn't find your results with this id"
    return render_template("resultat.html",
                            resultat_garb=table["garb"],
                            resultat_ext=table["ext"],
                            resultats_raw=table["raw"],
                            results_id=id_,
                            name=title)

@app.route("/iframes", methods = ['GET'])
@requires_auth
def iframes():

    id_ = str(request.args.get("id"))
    id_ = re.findall("[A-Za-z\d]+", id_)
    if not id_:
        return render_template("home.html")
    else:
        id_ = id_[0]
    try:
        with open(f"/tmp/streamFinder_{id_}.log", "r") as f:
            try:
                table = json.loads(f.read())
                links = table["garb"]
                title = table["title"]
            except Exception as e :
                print(f"Error in retrieving data -> {e}")
                links = []
                title = "Couldn't find your results with this id"
    except FileNotFoundError :
        print(f"Tried to find file with id {id_} but failed")
        links = []
        title = "Couldn't find your results with this id"
    return render_template("iframes.html",
                            results_id=id_,
                            links=links,
                            name=title)


if __name__ == "__main__":
    app.run()

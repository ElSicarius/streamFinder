#!/usr/bin/python3.7
import sys
import logging
import pathlib

path = str(pathlib.Path(__file__).parent.absolute()).split("streamFinder")[0]
sys.path.insert(1, path+"streamFinder/web/modules")
from streamFinder_web import app as application
logging.basicConfig(stream=sys.stderr)
application.secret_key = '1234'

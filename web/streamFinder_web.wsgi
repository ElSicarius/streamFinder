#!/usr/bin/python3.7
import sys
import logging

sys.path.insert(1, "/var/www/html/osintool/web/modules")
from streamFinder_web import app as application
logging.basicConfig(stream=sys.stderr)
application.secret_key = '1234'

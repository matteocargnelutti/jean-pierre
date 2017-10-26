#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

controllers/web.py - Web server : uses Flask
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os

from flask import Flask

from utils import Database
import models

#-----------------------------------------------------------------------------
# Routing
#-----------------------------------------------------------------------------
# Flask init
webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = models.Params().flask_secret_key

# Index
@webapp.route("/")
def hello():
    return "Hello World!"

# Flask run : Used by Gunicorn to launch the server
if __name__ == "__main__": 
    webapp.run()

#-----------------------------------------------------------------------------
# Controller
#-----------------------------------------------------------------------------
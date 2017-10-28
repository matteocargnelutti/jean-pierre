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
# Flask WSGI init and routes
#-----------------------------------------------------------------------------
# Flask init
webapp = Flask(__name__)

@webapp.route("/")
def hello():
    return "Hello World!"

#-----------------------------------------------------------------------------
# Controller
#-----------------------------------------------------------------------------
class Web:
    pass
    #
    # To do : loading secret key at startup !
    #
    # webapp.config['SECRET_KEY'] = params.flask_secret_key

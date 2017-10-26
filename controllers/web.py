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
from flask import Flask

from utils import Database
import models

#-----------------------------------------------------------------------------
# Routes
#-----------------------------------------------------------------------------
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

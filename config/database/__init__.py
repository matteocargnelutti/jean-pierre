#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

config/database - Initiates the SQlite database
"""
from database.params import Params
from database.groceries import Groceries
from database.products import Products
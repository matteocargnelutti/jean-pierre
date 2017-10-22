#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

config/database/products.py - Initiates the Products database
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Products class
#-----------------------------------------------------------------------------
class Products:
    """
    This class handles :
    Creation of a SQlite database for products cache
    """
    def __init__(self, link):
        """
        Constructor :
        Takes a link to a sqlite database as a parameter
        """
        self.link = link

    def create_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS products (
                    barcode CHAR (13) PRIMARY KEY,
                    name    TEXT,
                    pic     BLOB
                )
                WITHOUT ROWID;
                """
        self.link.execute(query)
        self.link.commit()
        return True

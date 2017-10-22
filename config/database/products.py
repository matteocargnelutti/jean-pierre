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
        Constructor : holds the link to the database.
        :param link: connector to a SQlite database
        :rtype: Params
        """
        self.link = link

    def create_table(self):
        """
        Creates the Products database
        :rtype: bool
        """
        query = """
                CREATE TABLE IF NOT EXISTS Products (
                    barcode CHAR (13) PRIMARY KEY,
                    name    TEXT,
                    pic     BLOB
                )
                WITHOUT ROWID;
                """
        self.link.execute(query)
        self.link.commit()
        return True

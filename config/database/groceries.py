#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

config/database/groceries.py - Initiates the Groceries database
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Groceries class
#-----------------------------------------------------------------------------
class Groceries:
    """
    This class handles :
    Creation of a SQlite database for groceries list
    """
    def __init__(self, link):
        """
        Constructor : holds the link to the database.
        :param link: connector to a SQlite database
        :rtype: Groceries
        """
        self.link = link

    def create_table(self):
        """
        Creates the Groceries database
        :rtype: bool
        """
        query = """
                CREATE TABLE IF NOT EXISTS Groceries (
                    barcode  CHAR (13) PRIMARY KEY,
                    quantity INT
                )
                WITHOUT ROWID;
                """
        self.link.execute(query)
        self.link.commit()
        return True

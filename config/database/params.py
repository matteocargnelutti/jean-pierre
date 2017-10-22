#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

config/database/params.py - Initiates the Params database
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Params class
#-----------------------------------------------------------------------------
class Params:
    """
    This class handles :
    Creation of a SQlite database for user parameters
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
        Creates the Params database
        :rtype: bool
        """
        query = """
                CREATE TABLE IF NOT EXISTS Params (
                    [key] TEXT PRIMARY KEY,
                    value TEXT
                )
                WITHOUT ROWID;
                """
        self.link.execute(query)
        self.link.commit()
        return True

    def add_item(self, key, value=""):
        """
        Adds a parameter into the database
        :param key: parameter key
        :param value: parameter value
        :type key: str
        :type value: str
        :rtype: bool
        """
        query = """
                INSERT INTO params VALUES (?, ?)
                """
        params = (key, value)
        self.link.execute(query, params)
        self.link.commit()
        return True

    def delete_item(self, key):
        """
        Deletes a parameter from the database
        :param key: parameter key
        :type key: str
        :rtype: bool
        """
        query = """
                DELETE FROM params WHERE `key` = ?
                """
        params = (key,)
        self.link.execute(query, params)
        self.link.commit()
        return True

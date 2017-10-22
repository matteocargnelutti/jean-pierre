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
        Constructor :
        Takes a link to a sqlite database as a parameter
        """
        self.link = link

    def create_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS params (
                    [key] TEXT PRIMARY KEY,
                    value TEXT
                )
                WITHOUT ROWID;
                """
        self.link.execute(query)
        self.link.commit()
        return True

    def add_item(self, key, value):
        query = """
                INSERT INTO params VALUES (?, ?)
                """
        params = (key, value)
        self.link.execute(query, params)
        self.link.commit()
        return True

    def delete_item(self, key):
        query = """
                DELETE FROM params WHERE `key` = ?
                """
        params = (key,)
        self.link.execute(query, params)
        self.link.commit()
        return True

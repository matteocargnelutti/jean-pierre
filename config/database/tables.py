#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

config/database/tables.py - Database operations
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from . import Connect

#-----------------------------------------------------------------------------
# ParamsTable class
#-----------------------------------------------------------------------------
class ParamsTable:
    """
    This class handles :
    Creation of a SQlite table for user parameters
    """
    def __init__(self):
        """
        Constructor
        :rtype: ParamsTable
        """
        # Is the database connexion initialized ?
        if not Connect.is_ready():
            Connect.on()

    def create(self):
        """
        Creates the Params table
        :rtype: bool
        """
        query = """
                CREATE TABLE IF NOT EXISTS Params (
                    [key] TEXT PRIMARY KEY,
                    value TEXT
                )
                WITHOUT ROWID;
                """
        Connect.LINK.execute(query)
        Connect.LINK.commit()
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
        Connect.LINK.execute(query, params)
        Connect.LINK.commit()
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
        Connect.LINK.execute(query, params)
        Connect.LINK.commit()
        return True

#-----------------------------------------------------------------------------
# ProductsTable class
#-----------------------------------------------------------------------------
class ProductsTable:
    """
    This class handles :
    Creation of a SQlite table for products cache
    """
    def __init__(self):
        """
        Constructor
        :rtype: ProductsTable
        """
        # Is the database connexion initialized ?
        if not Connect.is_ready():
            Connect()

    def create(self):
        """
        Creates the Products table
        :rtype: bool
        """
        query = """
                CREATE TABLE IF NOT EXISTS Products (
                    barcode CHAR (13) PRIMARY KEY,
                    name    TEXT,
                    pic     TEXT
                )
                WITHOUT ROWID;
                """
        Connect.LINK.execute(query)
        Connect.LINK.commit()
        return True

#-----------------------------------------------------------------------------
# GroceriesTable class
#-----------------------------------------------------------------------------
class GroceriesTable:
    """
    This class handles :
    Creation of a SQlite table for groceries list
    """
    def __init__(self):
        """
        Constructor
        :rtype: ProductsTable
        """
        # Is the database connexion initialized ?
        if not Connect.is_ready():
            Connect()

    def create(self):
        """
        Creates the Groceries table
        :rtype: bool
        """
        query = """
                CREATE TABLE IF NOT EXISTS Groceries (
                    barcode  CHAR (13) PRIMARY KEY,
                    quantity INT
                )
                WITHOUT ROWID;
                """
        Connect.LINK.execute(query)
        Connect.LINK.commit()
        return True

#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

scanner/database/tables.py
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import sqlite3
from database import Connect

#-----------------------------------------------------------------------------
# Params Table class
#-----------------------------------------------------------------------------
class ParamsTable:
    """
    This class handles :
    - Load and read parameters from the Params table as attributes
    Usage :
    - ParamsTable()
    - ParamsTable.PARAM_NAME
    """
    def __init__(self):
        """
        Constructor
        :rtype: ParamsTable
        """
        # Is the database connexion initialized ?
        if not Connect.is_ready():
            Connect.on()

        # Get all parameters
        try:
            Connect.CURSOR.execute("SELECT * FROM Params;")
            items = Connect.CURSOR.fetchall()
        except sqlite3.OperationalError as trace:
            raise Exception("Unable to reach the Params table : please run the config module ? \n" + trace)

        # Store parameters as attributes in lower caps as they are not constants
        for item in items:
            setattr(self, item['key'].lower(), item['value'])

        # Cast some parameters
        self.camera_res_x = int(self.camera_res_x)
        self.camera_res_y = int(self.camera_res_y)

#-----------------------------------------------------------------------------
# Groceries Table class
#-----------------------------------------------------------------------------
class GroceriesTable:
    pass

#-----------------------------------------------------------------------------
# Products Table class
#-----------------------------------------------------------------------------
class ProductsTable:
    """
    This class handles :
    - Add / Get items from the Products table, which is a cache for products info
    Usage :
    - products = ProductsTable()
    - product = products.get_one(barcode)
    """
    def __init__(self):
        """
        Constructor
        :rtype: ProductsTable
        """
        # Is the database connexion initialized ?
        if not Connect.is_ready():
            Connect.on()

    def get_item(self, barcode):
        """
        Get a product from its barcode
        :param barcode: barcode to lookup for
        :type barcode: string
        :rtype: tuple
        """
        query = "SELECT * FROM Products WHERE barcode = ?;"
        params = (barcode,)

        Connect.CURSOR.execute(query, params)
        product = Connect.CURSOR.fetchone()

        if product:
            return product
        else:
            return False

    def add_item(self, barcode, name):
        """
        Adds a product
        :param barcode: barcode to lookup for
        :type barcode: string
        :param name: name of the product
        :type name: string
        :rtype: bool
        """
        query = "INSERT INTO Products VALUES (?, ?, ?);"
        params = (barcode, name, "")

        Connect.CURSOR.execute(query, params)
        Connect.LINK.commit()

        return True

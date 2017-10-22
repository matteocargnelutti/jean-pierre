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
from database import Connect

#-----------------------------------------------------------------------------
# Params Table class
#-----------------------------------------------------------------------------
class ParamsTable:
    """
    This class handles :
    - Load and read parameters from the Params table as attributes
    Usage :
    - Params(link)
    - Params.PARAM_NAME
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
        Connect.CURSOR.execute("SELECT * FROM Params;")
        items = Connect.CURSOR.fetchall()

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
    pass

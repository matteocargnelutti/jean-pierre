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
    - Load and read parameters from the Params table
    - Parameters will be stored as CLASS attributes
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
            Connect()
        
        Connect.CURSOR.execute("SELECT * FROM Params;")
        items = Connect.CURSOR.fetchall()

        # Store parameters as class attributes in CAPS as they are constants
        for item in items:
            setattr(ParamsTable, item['key'].upper(), item['value'])

#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

scanner/database/params.py
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
    - Load and read parameters from the Params database
    - Parameters will be stored as CLASS attributes
    Usage :
    - Params(link) 
    - Params.PARAM_NAME
    """
    def __init__(self, link):
        """
        Constructor : loads parameters from the database
        :param link: connector to a SQlite database
        :rtype: Params
        """
        self.link = link
        self.cursor = self.link.cursor()

        self.cursor.execute("SELECT * FROM Params;")
        items = self.cursor.fetchall()

        # Store parameters as class attributes in CAPS as they are constants
        for item in items:
            setattr(Params, item['key'].upper(), item['value'])

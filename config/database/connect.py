#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

config/database/connect.py
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os
import sqlite3

#-----------------------------------------------------------------------------
# Connect class
#-----------------------------------------------------------------------------
class Connect:
    """
    This class handles :
    - Provides a link and a cursor to the database as class attributes
    Usage :
    - Connect.on()
    - Connect.CURSOR.execute(query, params)
    - ... etc
    - Connect.off()
    Available class attributes :
    - LINK
    - CURSOR
    - FILE (path to the database file)
    """
    @classmethod
    def on(cls, memory_mode=False):
        """
        Connect to the database
        :param memory_mode: If True, creates a temporary database in memory
        :rtype: bool
        """
        # Path to the database
        Connect.FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        Connect.FILE = Connect.FILE.replace('/config', '')
        Connect.FILE = Connect.FILE.replace('/scanner', '')
        Connect.FILE = Connect.FILE.replace('/web', '')
        Connect.FILE = Connect.FILE + "/database.db"

        if memory_mode:
            Connect.FILE = ':memory:'

        # Connect
        Connect.LINK = sqlite3.connect(Connect.FILE)
        Connect.LINK.row_factory = sqlite3.Row

        # Cursor
        Connect.CURSOR = Connect.LINK.cursor()

        return True

    @classmethod
    def off(cls):
        """
        Ends connection with the database.
        :rtype: bool
        """
        cls.LINK.close()
        cls.CURSOR = None
        return True

    @classmethod
    def is_ready(cls):
        """
        Is the connection open ?
        :rtype: bool
        """
        return cls.LINK != None

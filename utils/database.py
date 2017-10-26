#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

utils/cls.py - SQlite connector
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os
import sqlite3

#-----------------------------------------------------------------------------
# Database class
#-----------------------------------------------------------------------------
class Database:
    """
    This class handles :
    - Provides a link and a cursor to the database as class attributes
    Usage :
    - Database.on()
    - Database.CURSOR.execute(query, params)
    - ... etc
    - Database.off()
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
        Database.FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        Database.FILE =Database.FILE.replace('/utils', '')
        Database.FILE = Database.FILE + "/database.db"

        if memory_mode:
            Database.FILE = ':memory:'

        # Connect
        Database.LINK = sqlite3.connect(Database.FILE)
        Database.LINK.row_factory = sqlite3.Row

        # Cursor
        Database.CURSOR = Database.LINK.cursor()

        return True

    @classmethod
    def off(cls):
        """
        Ends connection with the cls.
        :rtype: bool
        """
        Database.LINK.close()
        Database.LINK = None
        Database.CURSOR = None
        return True

    @classmethod
    def is_ready(cls):
        """
        Is the connection open ?
        :rtype: bool
        """
        return Database.LINK != None

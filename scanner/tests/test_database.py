#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

scanner/tests/test_database.py - Units tests for the scanner app's database
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os

import database as db

#-----------------------------------------------------------------------------
# Tests for database package
#-----------------------------------------------------------------------------
class TestDatabase:
    """
    Tests setup, I/O operations on the database, following the app's rules.
    """

    def setup_method(self):
        """
        Creates a dummy database for tests
        """
        pass

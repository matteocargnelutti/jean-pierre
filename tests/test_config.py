#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

tests/test_config.py - Units tests for the config module
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os
import sqlite3

import config.database as database

#-----------------------------------------------------------------------------
# Tests for config/database/params
#-----------------------------------------------------------------------------
class TestParams:

    def setup_method(self):
        """
        Creates a dummy database for tests
        """
        database_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.database_path = database_path + "/database_test.db"
        self.link = sqlite3.connect(self.database_path)

    def teardown_method(self):
        """
        Deletes the dummy database
        """
        self.link.close()
        os.remove(self.database_path)

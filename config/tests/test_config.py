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

import database as db

#-----------------------------------------------------------------------------
# Tests for config.database module
#-----------------------------------------------------------------------------
class TestDatabase:

    def setup_method(self):
        """
        Creates a dummy database for tests
        """
        # Creates database
        db.Connect.on(memory_mode=True)
        self.cursor = db.Connect.CURSOR

        # Creates Params table
        self.params = db.ParamsTable()
        self.params.create()

        # Creates Groceries table
        self.groceries = db.GroceriesTable()
        self.groceries.create()

        # Creates Products table
        self.products = db.ProductsTable()
        self.products.create()

    def test_create_tables(self):
        """
        Tests the creation of the table Params, Groceries and Products
        """
        # Does the table exist ?
        self.cursor.execute("""
                            SELECT name FROM sqlite_master 
                            WHERE 
                                type='table' AND ( 
                                    name='Params' OR 
                                    name='Groceries' OR 
                                    name='Products' 
                                );
                            """)
        check = self.cursor.fetchall()
        assert len(check) == 3

    def test_params_add_item(self):
        """
        Tests the addition of a parameter with valid input
        """
        # Insert
        self.params.add_item('lorem', 'ipsum')

        # Has the value been added ?
        self.cursor.execute("""
                            SELECT * FROM Params
                            WHERE key = 'lorem' AND value = 'ipsum'
                            """)
        check = self.cursor.fetchone()
        assert check['key'] == 'lorem' and check['value'] == 'ipsum'

    def test_params_delete_item(self):
        """
        Tests the deletion of a parameter
        """
        # Insert and delete
        self.params.add_item('lorem', 'ipsum')
        self.params.delete_item('lorem')

        # Has the value been added ?
        self.cursor.execute("""
                            SELECT * FROM Params
                            WHERE key = 'lorem'
                            """)
        check = self.cursor.fetchone()
        assert not check

    def teardown_method(self):
        """
        Deletes the dummy database
        """
        # Disconnect
        db.Connect.off()

#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

tests/test_models.py - Units tests for the models
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os

from utils import Database
import models

#-----------------------------------------------------------------------------
# Tests for : Params model
#-----------------------------------------------------------------------------
class TestParamsModel:
    """
    Tests setup, I/O operations on the Params table, following the app's rules
    """

    def setup_method(self):
        """
        Creates a dummy database for tests
        """
        # Creates database
        Database.on(memory_mode=True)
        self.cursor = Database.CURSOR

        # Create table
        self.params = models.Params(autoload=False)
        self.params.create_table()

    def test_create_table(self):
        """
        Tests the creation of the table Params
        """
        # Does the table exist ?
        self.cursor.execute("""
                            SELECT name FROM sqlite_master 
                            WHERE type='table' AND name='Params';
                            """)
        check = self.cursor.fetchall()
        assert check

    def test_crud_item(self):
        """
        Tests basic operations on the Params table.
        Success conditions :
        - Ability to create an item
        - Ability to load an item
        - Ability to delete an item
        - The new item must be loaded as a Param's attribute
        """
        # Insert
        self.params.add_item('foo', 'bar')

        # Has the parameter been loaded as an attribute ?
        assert hasattr(self.params, 'foo')

        # Has the item been created ?
        param = self.params.get_item('foo')
        assert param['key'] == 'foo'

        # Delete
        self.params.delete_item('foo')
        assert not hasattr(self.params, 'foo') # Object attribute must have been deleted
        assert not self.params.get_item('foo') # Database entry must have disapeared

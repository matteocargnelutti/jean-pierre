#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

tests/test_models.py - Units tests for the models package
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os

import models
from utils import Database

#-----------------------------------------------------------------------------
# Tests for : Models
#-----------------------------------------------------------------------------
class TestModels:
    """
    Tests setup, I/O operations on the database following the app's rules
    """

    def setup_method(self):
        """
        Creates a dummy database for tests
        """
        # Creates database
        Database.on(memory_mode=True)
        self.cursor = Database.CURSOR

        # Create tables
        self.params = models.Params(autoload=False)
        self.products = models.Products()
        self.groceries = models.Groceries()
        self.params.create_table()
        self.products.create_table()
        self.groceries.create_table()

        # Insert dummy data
        self.default_barcode = '123456789ABCD'
        self.default_name = 'Lorem Ipsum'
        self.default_pic = 'PIC'

        self.params.add_item('foo', 'bar')
        self.products.add_item(self.default_barcode,
                               self.default_name,
                               self.default_pic)
        self.groceries.add_item(self.default_barcode, 1)

    def test_create_tables(self):
        """
        Tests the creation of the tables, as created in the setup method.
        Success conditions :
        - The three tables exist
        """
        # Does the table exist ?
        self.cursor.execute("""
                            SELECT 
                                name 
                            FROM 
                                sqlite_master 
                            WHERE 
                                type='table' AND (
                                name='Params' OR 
                                name='Groceries' OR 
                                name='Products' );
                            """)
        check = self.cursor.fetchall()
        assert len(check) == 3

    def test_get_item(self):
        """
        Test basic SELECT operations on the database,
        based on dummy data set in the setup method.
        Success conditions :
        - Ability to return a single item from Params (+ as an object attribute)
        - Ability to return a single item from Products
        - Ability to return a single item and a list from Groceries
        """
        # Params
        assert hasattr(self.params, 'foo')
        assert self.params.get_item('foo')['value'] == 'bar'

        # Products
        item = self.products.get_item(self.default_barcode)
        assert item['barcode'] == self.default_barcode
        assert item['name'] == self.default_name
        assert item['pic'] == 'PIC'

        # Groceries : single item (+ JOIN with Products)
        item = self.groceries.get_item(self.default_barcode)
        assert item['barcode'] == self.default_barcode
        assert item['name'] == self.default_name
        assert item['pic'] == 'PIC'
        assert item['quantity'] == 1

        # Groceries : list
        item = self.groceries.get_list()
        assert len(item) == 1
        assert item[self.default_barcode]['name'] == self.default_name
        assert item[self.default_barcode]['pic'] == 'PIC'
        assert item[self.default_barcode]['quantity'] == 1

    def test_add_item(self):
        """
        Tests basic INSERT operations on the database,
        based on dummy data set in the setup method.
        Success conditions :
        - Must have 1 item in the Params table, available as an object attribute
        - Must have 1 item in the Products table
        - Must have 1 item in the Groceries table
        """
        # Params
        assert hasattr(self.params, 'foo') # The param must have been set as an attribute when created previously
        assert self.params.get_item('foo')['value'] == 'bar' # Reload from database

        # Groceries and product : unique test as Groceries uses JOIN on product table
        item = self.groceries.get_item(self.default_barcode)
        assert item['barcode'] == self.default_barcode
        assert item['name'] == self.default_name
        assert item['pic'] == self.default_pic
        assert item['quantity'] == 1

    def test_edit_item(self):
        """
        Tests basic UPDATE operations on the database,
        based on dummy data set in the setup method.
        Success conditions :
        - Params' entry "foo" now equals "foobar"
        - Products' entry name is now "Dolor Sit Amet"
        - Groceries entry quantity is now 2
        """
        # Update
        self.params.edit_item('foo', 'foobar')
        self.products.edit_item(self.default_barcode, 'Dolor Sit Amet', 'PIC2')
        self.groceries.edit_item(self.default_barcode, 2)

        # Test
        assert self.params.foo == 'foobar'
        assert self.params.get_item('foo')['value'] == 'foobar'

        item = self.groceries.get_item(self.default_barcode)
        assert item['barcode'] == self.default_barcode
        assert item['name'] == 'Dolor Sit Amet'
        assert item['pic'] == 'PIC2'
        assert item['quantity'] == 2

    def test_delete_item(self):
        """
        Tests basic DELETE operations on the database,
        based on dummy data set in the setup method.
        Success conditions :
        - All three tables are freed from the deleted item
        """
        # Delete
        self.params.delete_item('foo')
        self.groceries.delete_item(self.default_barcode)
        self.products.delete_item(self.default_barcode)

        # Test
        assert not hasattr(self.params, 'foo')
        assert not self.params.get_item('foo')
        assert not self.products.get_item(self.default_barcode)
        assert not self.groceries.get_item(self.default_barcode)


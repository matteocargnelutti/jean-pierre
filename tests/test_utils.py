#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

tests/test_utils.py - Units tests for the utils package
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os

import models
import utils
from utils import Database

#-----------------------------------------------------------------------------
# Tests for : Utils.FindProduct
#-----------------------------------------------------------------------------
class TestFindProduct:
    """
    Tests for the FindProduct tool.
    This tool is threaded.
    """

    def setup_method(self):
        """
        Setup method, creates a dummy database
        """
        # Creates database
        Database.on(is_test=True)
        self.cursor = Database.CURSOR

        # Create tables
        self.params = models.Params(autoload=False)
        self.products = models.Products()
        self.groceries = models.Groceries()
        self.params.create_table()
        self.products.create_table()
        self.groceries.create_table()

        # Defaults
        self.valid_barcode = '3017620424403'
        self.invalid_barcode = '123456789ABCD'

        # Deconnects database to let threads use them
        Database.off()

    def teardown_method(self):
        """
        Cleans up dummy database after each test
        """
        Database.off()
        os.remove(Database.PATH + Database.DATABASE_TEST)

    def test_run_valid(self):
        """
        Tests FindProduct process with both valid and invalid inputs
        Success conditions :
        - Valid input : an item has been added to the Products and Groceries databases
        - Invalid input : no item has been added to the Products nor the Groceries databases
        """
        # Launch threads
        thread_valid = utils.FindProduct(self.valid_barcode, is_test=True)
        thread_valid.start()

        thread_invalid = utils.FindProduct(self.invalid_barcode, is_test=True)
        thread_invalid.start()

        thread_valid.join()
        thread_invalid.join()

        # Tests
        Database.on(is_test=True)
        assert self.groceries.get_item(self.valid_barcode)
        assert not self.groceries.get_item(self.invalid_barcode)
